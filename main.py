from gtts import gTTS
from art import tprint
import pdfplumber
from pathlib import Path


def pdf_to_mp3(file_path='test.pdf', language='en'):
    """
    Функция конвертирует pdf файл в аудио запись.
    Пользователь указываю путь до файла, и язык текста, на выходе mp3 файл.
    """

    if Path(file_path).is_file() and Path(file_path).suffix == '.pdf':
        #return 'File exists!'


        print(f'[+] Original file: {Path(file_path).name}')
        print('[+] Proccessing...')

        # открывает pdf файл с помошью модуля pdfplumber
        with pdfplumber.PDF(open(file=file_path, mode='rb')) as pdf:
            # распоковывает страницы
            pages = [page.extract_text() for page in pdf.pages]

        # обьединяет страницы
        text = ''.join(pages)
        # убирает переходы на страницы, обьединяя в одну строчку
        text = text.replace('\n', '')

        # функция преобразовывает текст в мп3 файл
        my_audio = gTTS(text=text, lang=language, slow=False)
        # получаем имя файла с помощью свойства stem
        file_name = Path(file_path).stem
        # сохраняем файл
        my_audio.save(f'{file_name}.mp3')

        return f'[+] {file_name}.mp3 saved successfully'

    else:
        return 'File not exists, check the file path!'


def main():
    tprint('pdf>>TO>>MP3', font='bulbhead')
    file_path = input("Enter a file's path: ")
    language = input("Choose language, for example 'en' or 'ru': ")
    print(pdf_to_mp3(file_path=file_path, language=language))


if __name__ == '__main__':
    main()

