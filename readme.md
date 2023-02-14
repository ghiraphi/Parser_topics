## Парсер по списку сайтов с использованием selenium и pdf2image. 


#### На входе пользователь указывает:
1) список сайтов .txt
2) словари для поиска. В этой реализации используется два справочника (.txt) со списком строк (объект и действие). Они генерируются между собой - создают общий словарь, по нему проходит анализ сайтов по заданной тематике. В перспективе можно создать набор правил по количеству справочников и их сочетанию друг с другом + использовать регулярки regex.

#### На выходе пользователь получает:
Таблицу csv с ссылками на страницы каждого сайта, где найдена тема. Также пользователь получает список строк словаря, по которым найдена тема. 


### install
__must be downloaded__:\
Poppler-0.68.0\
Tesseract-OCR\
ChromeDriver 


git clone https://github.com/ghiraphi/parser_topic.git  
cd parser_topic\
pip install traceback\
pip install selenium\
pip install urllib\
pip install pandas\
pip install re\
pip install request\
pip install bs4import \
pip install pdf2image\
pip install urllib\
pip install itertools
python main.py
