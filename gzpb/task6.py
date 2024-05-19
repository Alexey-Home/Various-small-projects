# Имеется банковское API возвращающее JSON
# {
# 	"Columns": ["key1", "key2", "key3"],
# 	"Description": "Банковское API каких-то важных документов",
# 	"RowCount": 2,
# 	"Rows": [
# 		["value1", "value2", "value3"],
# 		["value4", "value5", "value6"]
# 	]
# }
# Основной интерес представляют значения полей "Columns" и "Rows",
# которые соответственно являются списком названий столбцов и значениями столбцов
#
# Задание:
# 	1. Получить JSON из внешнего API
# 		ендпоинт: GET https://api.gazprombank.ru/very/important/docs?documents_date={"начало дня сегодня в виде таймстемп"}
# 	2. Валидировать входящий JSON используя модель pydantic
# 		(из ТЗ известно что поле "key1" имеет тип int, "key2"(datetime), "key3"(str))
# 	2. Представить данные "Columns" и "Rows" в виде плоского csv-подобного pandas.DataFrame
# 	3. В полученном DataFrame произвести переименование полей по след. маппингу
# 		"key1" -> "document_id", "key2" -> "document_dt", "key3" -> "document_name"
# 	3. Полученный DataFrame обогатить доп. столбцом:
# 		"load_dt" -> значение "сейчас"(датавремя)


from flask import Flask, jsonify
from flask_restful import Api, Resource
import json
import requests
import time
import pandas as pd


app = Flask(__name__)
api = Api(app)

from pydantic import BaseModel, ValidationError
from datetime import datetime
from typing import List


class RowData(BaseModel):
    key1: int
    key2: datetime
    key3: str


class InputData(BaseModel):
    Columns: List[str]
    Description: str
    RowCount: int
    Rows: List[List[RowData]]


def valid_json(json_data):
    try:
        data = InputData.model_validate(json_data)
        return data.model_dump()
    except ValidationError as e:
        return {"error": e.errors()}


class Documents(Resource):
    def __init__(self):
        self.session = requests.session()

    def get(self):

        time_day = int(
            time.mktime(time.localtime()) - time.localtime().tm_sec- 60 * time.localtime().tm_min- 3600 * time.localtime().tm_hour
        )
        url = f"https://api.gazprombank.ru/very/important/docs?documents_date={time_day}"

        response = self.session.get(url, timeout=200)
        if response.status_code == 200:
            data = response.json()
            validate_data = valid_json(data)
            df = pd.DataFrame(validate_data)
            csv_file = df.melt(var_name="Columns", value_name="Rows")

            col_map = {
                "key1": "document_id",
                "key2": "document_dt",
                "key3": "document_name",
            }
            renamed_df = csv_file.rename(columns=col_map)

            now = pd.Timestamp.now()
            enriched_df = renamed_df.assign(load_dt=now)
            records = enriched_df.to_dict(orient="records")
            json_data = json.dumps(records)
            return jsonify(json_data)
        else:
            return "Error", response.status_code


api.add_resource(Documents, "/get_docks")



if __name__ == "__main__":
    app.run(debug=True)
