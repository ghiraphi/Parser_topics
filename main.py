#все ссылки сайта
import traceback
import time
from urllib.parse import urlparse, urljoin
from itertools import *
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import InvalidArgumentException
from selenium.common.exceptions import WebDriverException
import pandas as pd
from selenium.webdriver import *
from selenium.webdriver.common.by import By
from selenium import webdriver
import urllib
from pdf2image import convert_from_path  # конвертер пдф в картинки
import re
import requests
from bs4 import BeautifulSoup
import urllib.request

# Сброс ограничений на количество выводимых рядов
pd.set_option('display.max_rows', None)
# Сброс ограничений на число столбцов
pd.set_option('display.max_columns', None)
# Сброс ограничений на количество символов в записи
pd.set_option('display.max_colwidth', None)

def bad_pdf(link):
    import os, glob
    import time
    from selenium import webdriver
    import urllib.parse as urlparse
    import posixpath
    stats = os.stat('work_file.pdf')
    razmer = stats.st_size
    print('размер', razmer)

    if razmer < 10000:
        for file in glob.glob("pdf_folder\\*"):
            os.remove(file)
            print("Deleted " + str(file))
        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', {
            "download.default_directory": "pdf_folder\\",  # Change default directory for downloads
            "download.prompt_for_download": False,  # To auto download the file
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True  # It will not show PDF directly in chrome
        })
        driver = webdriver.Chrome('C:\\Users\piolv\Desktop\chromedriver.exe', chrome_options=options)
        driver.get(link)
        path = urlparse.urlsplit(link).path
        filename = posixpath.basename(path)

        #time.sleep(10)
        driver.quit()
        import os
        oldfile = os.listdir('pdf_folder\\')[0]
        print('имя файла1-', oldfile)
        os.rename(os.path.join(f"pdf_folder\\", f"{oldfile}"), os.path.join(f"pdf_folder\\", "work_file.pdf"))
def bad_pdf_nosize(link):
    zvonok=0
    import os, glob
    import time
    from selenium import webdriver
    import urllib.parse as urlparse
    import posixpath
    for file in glob.glob("pdf_folder\\*"):
        os.remove(file)
        print("Deleted " + str(file))
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {
        "download.default_directory": "pdf_folder\\",  # Change default directory for downloads
        "download.prompt_for_download": False,  # To auto download the file
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True  # It will not show PDF directly in chrome
    })
    driver = webdriver.Chrome('C:\\Users\piolv\Desktop\chromedriver.exe', chrome_options=options)
    try:
        driver.get(link)
        path = urlparse.urlsplit(link).path
        filename = posixpath.basename(path)

        #time.sleep(10)
        driver.quit()
        import os
    except:
        traceback.print_exc()
        zvonok = 1
    try:
        oldfile = os.listdir('pdf_folder\\')[0]
        print('имя файла2-', oldfile)
        os.rename(os.path.join(f"pdf_folder\\", f"{oldfile}"), os.path.join(f"pdf_folder\\", "work_file.pdf"))
    except IndexError:
        traceback.print_exc()
        zvonok = 1
    return zvonok
def orkrivalka_google(site):
    # Открываем браузер
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    # options.add_argument('--remote-debugging-port=9222')
    options.add_argument('--enable-javascript')
    options.add_argument("--user-agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0'")
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-insecure-localhost')
    driver = webdriver.Chrome('C:\\Users\piolv\Desktop\chromedriver.exe', chrome_options=options)
    # Переходим по ссылке
    driver.set_page_load_timeout(5)
    driver.get('https://www.google.com/')
    # Находим на странице поле ввода поискового запроса
    search_bar = driver.find_element(By.NAME, "q")
    # Очищаем поле
    search_bar.clear()
    # Вводим запрос
    search_bar.send_keys(f'политика персональных site:{site}')
    # Имитируем нажатие кнопки Enter
    search_bar.send_keys(Keys.RETURN)
    # Получаем код страницы
    body = driver.find_element(By.TAG_NAME, "body")
    html = body.get_attribute('innerHTML')
    soup = BeautifulSoup(html, features="lxml")
    soup = soup.find_all('a')
    soup2 = BeautifulSoup(html, features="lxml")
    soup2 = soup2.find_all('div', class_='kvH3mc BToiNc UK95Uc')
    slovar_google = {}
    for i in soup2:
        if re.search('персональных', i.text.lower()):
            print('найдено упоминание персональных')
            text_link = i.text.lower()
            text_link = re.sub(r"\W", " ", text_link).lower()
            text_link = re.sub(r"\s+", " ", text_link)
            teg_a = i.find('a')
            slovar_google[teg_a.get("href")] = text_link
    driver.quit()
    # print(slovar_google)
    return slovar_google
def esli_pdf(link):
    print('принял файл, перевожу в картинки', link)
    try:
        from PIL import Image
    except ImportError:
        import Image
    import pytesseract

    def ocr_core(filename):  # распознователь текста из фото
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
        text = pytesseract.image_to_string(Image.open(filename), lang='rus')
        return text

    text_pdf = []

    pages = convert_from_path(f'{link}', 300, poppler_path=r'C:\poppler-0.68.0\bin')
    print('конвертирую картинки в текст=====================- ', link)
    for i, page in enumerate(pages):
        page.save(f'pdf_folder\\out{i}.jpg', 'JPEG')
        chast = ocr_core(f'pdf_folder\\out{i}.jpg')
        text_pdf.append(chast)
        if i==7:
            break
    text_pdf = ' '.join(text_pdf)

    text_pdf = re.sub(r"\W", " ", text_pdf).lower()
    text_pdf = re.sub(r"\s+", " ", text_pdf)
    # print(text_pdf)
    return text_pdf
def robot(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--enable-javascript')
    options.add_argument("--user-agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0'")
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-insecure-localhost')
    driver = webdriver.Chrome('C:\\Users\piolv\Desktop\chromedriver.exe', chrome_options=options)
    url = url.encode('ascii', 'ignore').decode('unicode_escape')

    try:
        print('без искла')
        driver.set_page_load_timeout(10)
        driver.get(url)
        html = driver.page_source
        #print(html)
    except InvalidArgumentException:
        print('искл1')
        driver.set_page_load_timeout(60)
        driver.get(url)
        html = driver.page_source
        # #driver.quit()
    except TimeoutException:
        print('сайт долго не открывается')
        html = driver.page_source
        driver.quit()
    except WebDriverException:
        print('сайт не открывается, ошибка доступа')
        html = '-'
        pass
    return html
def analiz(kluch, text):
    lampa = 0


    kluch = kluch.replace("*", "\w*").replace("[а-я]", "\w").replace("[0-9]", "\d").replace("[0-9]", "\d").replace(".", "\w")
    #print('до вайла', kluch)
    while re.search(' \d+,\d+ ', kluch):
        start = re.search(' \d+,\d+ ', kluch).start()
        end = re.search(' \d+,\d+ ', kluch).end()
        #print(start, end, kluch[start + 1:end - 1])
        rasst = kluch[start + 1:end - 1].split(',')
        kluch = kluch[:start] + '( (\w|-)+){' + rasst[0] + ',' + rasst[1] + '} ' + kluch[end:]
    #print(kluch)

    try:
        nashalo = re.search(kluch, text).start()  # начало куска текста, где нашлось
        konec = re.search(kluch, text).end()  # конец куска текста, где нашлось
        #print(text[nashalo:konec])
        lampa = 1
    except AttributeError:
        pass
        #print('None')
    return lampa
def spisok_kluchey(spr1, spr2):
    def generator_strok(base_line):
        esheodin = []
        while '|' in base_line:
            # print('007')
            spis_strok = base_line.split(',')
            spis_strok = list(set(spis_strok))
            for indexstr, stroka in enumerate(spis_strok):
                if '|' in stroka:
                    # print(len(esheodin),  len(spis_strok) )
                    if re.search('\(\S+ ', stroka):
                        while re.search('\(\S+ ', stroka) or re.search(' \S+\)', stroka) or re.search(' \S+\|', stroka) or re.search('\|\S+ ', stroka):
                            for bukva in range(len(stroka)):
                                if (re.fullmatch('\(', stroka[bukva])) and re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|@|<|>|\-|_|\?|\*|\[|\]|\.|\+|\|)', stroka[bukva + 1]):  # если в строке скобка
                                    start = bukva  # фиксация начала скобки со знаком вопроса
                                    continue
                                if (re.fullmatch('\)', stroka[bukva])) and re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|@|<|>|\-|_|\?|\*|\[|\]|\.|\+|\|)', stroka[bukva - 1]):  # если в строке скобка
                                    end = bukva  # фиксация начала скобки со знаком вопроса
                                    break
                            skobka = stroka[start:end + 1]
                            if re.search('\(\S+ ', skobka) or re.search(' \S+\)', skobka) or re.search(' \S+\|', skobka) or re.search('\|\S+ ', skobka):
                                skobka = skobka.replace(' ', '_').replace('(', '<').replace(')', '>').replace('|', '&')
                                stroka = stroka[:start] + skobka + stroka[end + 1:]
                            else:
                                skobka = skobka.replace('(', '<').replace(')', '>').replace('|', '&')
                                stroka = stroka[:start] + skobka + stroka[end + 1:]
                        stroka = stroka.replace('<', '(').replace('>', ')').replace('&', '|')
                    spis_slov = stroka.split()
                    for slovo in spis_slov:  # определяем кусок со скобкой
                        if re.match('\)\S*', slovo) or re.match('\S*\(', slovo):
                            slovo = list(slovo)
                            for bukva in range(len(slovo)):
                                if re.fullmatch('\(', slovo[bukva]) and re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|@|<|>|\-|_|\?|\*|\[|\]|\.|\+|\|)', slovo[bukva + 1]):  # если в строке скобка
                                    start = bukva  # фиксация начала скобки со знаком вопроса
                                    continue
                                if re.fullmatch('\)', slovo[bukva]) and re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|@|<|>|\-|_|\?|\*|\[|\]|\.|\+|\|)', slovo[bukva - 1]):  # если в строке скобка
                                    end = bukva  # фиксация начала скобки со знаком вопроса
                                    break
                            slovo = ''.join(slovo)
                            skobka = slovo[start:end + 1]
                            skobka = skobka.replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace("'", '')
                            slova_v_skobke = skobka.split('|')  # сделали варианты внутри скобки. добавили в новый список
                            slova_v_skobke.insert(0, spis_slov.index(slovo))  # добавили индекс
                            kolvo_slov_v_skob = len(slova_v_skobke) - 1  # минусуем на один, потому что один из элементов - это индекс. а нам надо знать точно количество слов
                            break
                    new_stroki_vmeste = []

                    for nomer_slova_v_skob in range(0, kolvo_slov_v_skob):
                        new_stroka = []
                        for indexslova, slovo in enumerate(spis_slov):
                            if '|' not in slovo:
                                new_stroka.append(slovo)
                            if '|' in slovo:
                                if indexslova == slova_v_skobke[0]:
                                    vrem1 = []
                                    vrem1.append(slovo[:start])
                                    vrem1.append(slova_v_skobke[nomer_slova_v_skob + 1])
                                    vrem1.append(slovo[end + 1:])
                                    new_stroka.append(''.join(vrem1))
                                else:
                                    new_stroka.append(slovo)
                        new_stroki_vmeste.append(' '.join(new_stroka))
                    for new_stroka_vmeste in new_stroki_vmeste:
                        new_stroka_vmeste = new_stroka_vmeste.replace('_', ' ')
                        if '|' not in new_stroka_vmeste:
                            esheodin.append(new_stroka_vmeste)
                            # print(len(esheodin), 'ещё один список')

                        else:
                            spis_strok.append(new_stroka_vmeste)

                    spis_strok[indexstr] = '$'
                    spis_strok = list(set([k for k in spis_strok if k != '$']))
                    break
            base_line = ','.join(spis_strok)
            if spis_strok == []:
                base_line = list(set(esheodin))
        if type(base_line) == str:
            base_line = [base_line]
        return base_line
    with open(spr1, "r", encoding="utf-8") as f:
        spar1 = f.read()
        spar1 = spar1.split('\n')
    with open(spr2, "r", encoding="utf-8") as f:
        spar2 = f.read()
        spar2 = spar2.split('\n')

    kluchi = []
    for i in range(len(list(list(product(spar1, spar2))))):
        element = list(list(product(spar1, spar2))[i])
        element = '$'.join((str(x) for x in element))
        element = element.replace('$', ' 0,50000 ').replace('\xa0', ' ').replace('\ufeff', '').replace(',', '£')
        for i in generator_strok(element):
            i = i.replace('£', ',')
            kluchi.append(i)
    for i in range(len(list(list(product(spar2, spar1))))):
        element = list(list(product(spar2, spar1))[i])
        element = '$'.join((str(x) for x in element))
        element = element.replace('$', ' 0,50000 ').replace('\xa0', ' ').replace('\ufeff', '').replace(',', '£')
        for i in generator_strok(element):
            i = i.replace('£', ',')
            kluchi.append(i)
    kluchi=list(set(kluchi))
    print(len(kluchi),'-сколько всего ключей есть из двух справочников')
    return kluchi
def analizator(spr1, spr2, text):
    # coding: utf-8

    text = re.sub(r"\W", " ", text).lower()
    text = re.sub(r"\s+", " ", text)
    print('начал работу анализатор, текст для работы, отрывок---   ',text[:1000])

    kluchi=spisok_kluchey(spr1, spr2)
    def validnost(kluch, text):
        kluch = kluch.replace("*", ".*").replace("[а-я]", "\w").replace("[0-9]", "\d").replace("[0-9]", "\d")
        while re.search('[^0-9] [^0-9]', kluch):
            start = re.search('[^0-9] [^0-9]', kluch).start() + 1
            kluch = kluch[:start + 1] + '0,0 ' + kluch[start + 1:]

        kluch = kluch.split()

        newtext = text.split()
        counter = 0
        for slovo in kluch:  # проверка - сколько пар слов в ключе
            if kluch.index(slovo) != len(kluch) - 1:  # не равен последнему элементу
                if kluch.index(slovo) == 0 or kluch.index(slovo) % 2 == 0:  # выбирает все элементы со словами без расстояния
                    counter += 1  # сколько слов- пар в ключе
        nachslovo_kluch = [index_i for index_i, i in enumerate(newtext) if re.fullmatch(kluch[0], i)]  # сколько раз найдётся первое слово из ключа

        signal_stop = 0
        if len(nachslovo_kluch) > 0:
            for fragment in nachslovo_kluch:
                if signal_stop == 1:
                    break
                podsch = 0
                text = newtext[fragment:]  # начинаем с первого ключа
                # print('fragment---------', fragment, nachslovo_kluch, kluch[0], text)
                for slovo in kluch:
                    if kluch.index(slovo) != len(kluch) - 1:  # не равен последнему элементу
                        if kluch.index(slovo) == 0 or kluch.index(slovo) % 2 == 0:  # выбирает все элементы со словами без расстояния
                            # print(slovo, kluch[kluch.index(slovo)+2], re.search(f'( |^){slovo}( |$)', ' '.join(text)), re.search(f'( |^){kluch[kluch.index(slovo)+2]}( |$)', ' '.join(text)), ' '.join(text))
                            if re.search(f'( |^){slovo}( |$)', ' '.join(text)) and re.search(f'( |^){kluch[kluch.index(slovo) + 2]}( |$)', ' '.join(text)):  # если ближайшее и следующее слова в тексте,то
                                ind1 = [text.index(i) for i in text if re.fullmatch(slovo, i)][0]  # индексы слов, где нашлось
                                # print('ind1', ind1, slovo, text)
                                pochti_ind1 = [index_i for index_i, i in enumerate(text) if re.fullmatch(slovo, i)]
                                pochti_ind2 = [index_i for index_i, i in enumerate(text) if re.fullmatch(kluch[kluch.index(slovo) + 2], i)]
                                # print('+++++pochti_ind2--',ind1, pochti_ind2, slovo, kluch[kluch.index(slovo)+2], kluch)
                                for i in pochti_ind2:
                                    if i > ind1:
                                        ind2 = i
                                        break

                                ras1 = int(kluch[kluch.index(slovo) + 1][:1])
                                ras2 = int(kluch[kluch.index(slovo) + 1][2:])
                                razind = int(ind2 - ind1 - 1)
                                # print('===перед условиями-',slovo, ras1, '--', ind2, ind1, '--', razind, '--', ras2, counter, podsch, text, slovo, kluch[kluch.index(slovo)+2])
                                if ras1 <= razind <= ras2:  # если оно подходит под расстояние
                                    podsch += 1  # подсчёт, сколько подходит под условия расстояния
                                    # print('===оценка-',slovo, ras1,  '--', ind2, ind1, '--',razind, '--', ras2, counter, podsch)
                                    if counter == podsch:
                                        signal_stop = 1
                                        # print('валидно')
                                        break
                                else:
                                    # print('не валидно, потому что не входит в расстояние в тексте', ras1,razind,ras2, slovo, kluch[kluch.index(slovo)+2], ind2, ind1)
                                    break
                            else:
                                # print('не валидно, потому что нет одного из слов пары в тексте')
                                break
                    if kluch.index(slovo) == len(kluch) - 1:
                        # print('не валидно, потому что конец ключа и ничего не нашлось в тексте')
                        break

        else:
            # print('не валидно, потому что не найдено первое слово ключа в тексте')
            pass
        return signal_stop


    metka=0
    rez_an=[]
    sp_kl=[]
    kolvo=0
    for i in kluchi:
        if kolvo>5:
            break
        kluch = i.replace(u'\xa0', u' ')
        if analiz(kluch, text) == 1:
            metka = 1
            kolvo += 1
            sp_kl.append(i)

            print(i, '   --ключ ', kluchi.index(i))
        if kluchi.index(i)==len(kluchi)-1 and metka==0:
            print('осморены все ключи и ни один не подпадает под текст - ', text[:5000], '/nвот ключи - ', kluchi[:100])

    rez_an.append(metka)
    rez_an.append(sp_kl)
    return rez_an
def proverkapdf(url):
    opoznavatel=0

    try:
        session_obj = requests.Session()
        response = session_obj.get(url, headers={"User-Agent": "Mozilla/5.0"}, verify=False)
        print(response)
        tiphead=response.headers['Content-Type']
        print(tiphead, type(tiphead))
    except:
        import ssl
        from urllib3 import poolmanager
        class TLSAdapter(requests.adapters.HTTPAdapter):
            def init_poolmanager(self, connections, maxsize, block=False):
                """Create and initialize the urllib3 PoolManager."""
                ctx = ssl.create_default_context()
                ctx.set_ciphers('DEFAULT@SECLEVEL=1')
                self.poolmanager = poolmanager.PoolManager(
                    num_pools=connections,
                    maxsize=maxsize,
                    block=block,
                    ssl_version=ssl.PROTOCOL_TLS,
                    ssl_context=ctx)

        session = requests.session()
        session.mount(url, TLSAdapter())
        res = session.get(url, allow_redirects=False)
        tiphead = res.headers['Content-Type']
        print(tiphead, type(tiphead))
    if 'application' in tiphead and ('download' in tiphead or 'pdf' in tiphead):
        opoznavatel=1
        print('да, содержит пдф продолаю')
        return opoznavatel
rezult = []
def otkrivalka(url):
    global rezult
    tip_mat=0
    soup = BeautifulSoup(robot(url), features="lxml") #СОБИРАЕТ ВСЕ ССЫЛКИ НА ГЛАВНОЙ СТРАНИЦЕ
    print(len(str(soup)), str(soup)[:100]  )
    print( 'есть суп')
    if '[0-9][0-9][0-9] Forbidden' in str(soup) or '<html><body><p>-</p></body></html>' in str(soup):
        print('XXX Forbidden')
        rezult.append({"название источника": url, "название страницы": '', "ссылка на страницу": '', "тип источника": 'Сайт не работает', "отработавшие ключи": ''})
        return
    print('переход дальше')
    ob=soup.find_all('a') #все сссылки на главной странице, список
    print('ссылки с тегом а найдены-', ob)
    #time.sleep(2)
    list_link1=[]
    list_after1=[]
    ob =list(set(ob))
    print('список ссылок до перебора-', len(ob))
    for i in ob: #перебор каждой ссылки                                      #ПЕРЕБИРАЕТ КАЖДУЮ НАЙДЕННУЮ ССЫЛКУ, ПРОВЕРЯЕТ, ЕСТЬ ЛИ В НЕЙ УЖЕ ТЕКСТ ДОКУМЕНТА ИЛИ ПДФ.ФАЙЛ ДОКУМЕНТА
        print('начинается самое начало перебора ссылок на главной странице=====', url, '---',i, '\n',ob.index(i),len(ob) )
        href = i.get("href")
        href = str(href)
        url = str(url)


        print('перед решением правильной ссылки ---', url, '-',href, '-', type(url), '-', type(href))
        url=url.replace(' ','')
        url = url.replace("'", "%27")
        href = href.replace(' ', '%20')
        href = href.replace("'", "%27")
        url = re.sub('[\t\r\n]', '', url)
        href = re.sub('[\t\r\n]', '', href)

        try:
            if href[0]=='/' and href[len(href)-1]=='/' and url[len(url)-1]=='/':
                href = url + href[1:]
            else:
                gik = urljoin(url, href)
                print(' разные1++++++++++++++++++++ соединяю', gik)
                href = gik
            href = href.split('#')[0]
        except:
            href=str(href)
            print(' одинаковые++++++++++++++++++++ не соединяю1',  href)
            href = url
        print('1==-ссылки первый перебор идёт                                  ', url, href)
        if re.search('(.*правов.*|.*информа.*|.*полит.*|.*конфид.*|.*документ.?.?|.*соглашен.*|.*данных.*|.*персональн.*|.*правила.*|.*оферт.*)', i.text.lower()) and href!=url: #находит все ссылки связанные, с доками
            print('первый уровень - ссылка и название - поймались по близким словам---   ',url, href, i.text.lower())


            print('\n\n проверяю на точность - персональные или нет -=====',href, i.text)
            if re.search('(.*персональных данных.*|.*политик.* .*конф.*|правила пользования сайтом|публичная оферта|конфиденциальность|.*политика обработки.*)', i.text.lower()): #если есть такая формулировка открываем один раз, далее не идём
                print('прямая ссылка1==содержатся точные слова с персом',url, href, '-', i.text)
                if re.search('(.*\.(pdf|PDF))', href) or proverkapdf(href)==1: # если пдф файл - сохраняет - конвертирует в фото - конвертирует в текст - выдаёт текст
                    print('это пдф, начинаю смотреть внутрь', href)

                    destination = 'work_file.pdf'
                    url0 = href
                    #url0 = urllib.parse.quote_plus(url0)
                    print(url0, ' url0//**')
                    url0 = url0.replace('%3A', ':')
                    try:
                        urllib.request.urlretrieve(url0, destination)

                        bad_pdf(url0)
                        print('\nсохранил файл')

                        text=esli_pdf('work_file.pdf')
                        save_anal=analizator("spar1.txt", "spar2.txt", text)
                        if save_anal[0]==1:
                            tip_mat = 'pdf'
                            rezult.append({"название источника": url, "название страницы": re.sub(r"\s", " ", i.text), "ссылка на страницу": href, "тип источника": tip_mat, "отработавшие ключи": '\n'.join(save_anal[1])})
                            return print('найден пдф на первом уровне', href, i.text, url)
                        else:
                            list_after1.append(href.split('#')[0])
                            print('не нашелся документ 1 уровень - создаём список-- ', list_after1)
                    except:
                        print(Exception, 'ошибка' )
                        pass
                else: # если будет найден сам словарь , то всё хватит , стоп
                    text=re.sub(r"\s+", " ", BeautifulSoup(robot(href), features="lxml").find('html').text)
                    print('не пдф - возможно, прямо в тексте в этой ссылке1---  ',text[:1000])
                    # анализ по сайту, используя словарь
                    save_anal = analizator("spar1.txt", "spar2.txt", text)
                    if save_anal[0]==1:
                        tip_mat = 'text'
                        rezult.append({"название источника": url, "название страницы": re.sub(r"\s", " ", i.text), "ссылка на страницу": href, "тип источника": tip_mat, "отработавшие ключи": '\n'.join(save_anal[1])})
                        return print('найден текст на первом уровне', href, i.text, url)
                    else:
                        list_after1.append(href.split('#')[0])
                        print('не нашелся текст на странице  1 уровень - создаём список-- ', list_after1)
                        if href not in list_link1 and re.search('(.*\.(pdf|PDF))', href)==None:
                            list_link1.append(href)
                            print('**+* текст не нашёлся, но добавляем ещё одну ссылку в первый список-- - ', href, list_link1)
            else:
                if href not in list_link1 and re.search('(.*\.(pdf|PDF))', href)==None:
                    list_link1.append(href)
                    print('не персональные. **+* нашлись похожие слова в  ссылках, но персональных не было, поэтому добавляем ещё одну ссылку в первый список-- - ', href, list_link1)
    print('на первом уровне ничего не нашлось, перехожу глубже - на второй уровень, буду изучать ссылки - \n', list_link1)
    for deep_link in list_link1:
        print('ссылка второго уровня -', deep_link)
        soup2 = BeautifulSoup(robot(deep_link), features="lxml")
        ob2 = soup2.find_all('a')  # все сссылки на главной странице, список
        list_link2 = []
        print('перебор ссылок второго уровня-', deep_link)
        for i2 in ob2:  # перебор каждой ссылки
            href2 = i2.get("href")
            href2 = str(href2)

            print('начинается строка2===+=', ob2.index(i2), len(ob2), href2)
            if re.search('(.*правов.*|.*информа.*|.*полит.*|.*конфид.*|.*документ.?.?|.*соглашен.*|.*данных.*|.*персональн.*|.*правила.*|.*оферт.*)', i2.text.lower()):  # находит все ссылки связанные, с доками
                try:
                    if url[0:4] != href[1:5] or href2 == None:
                        href2 = urljoin(deep_link, href2)
                except TypeError:
                    href2 = str(href2)
                print('href2--', href2)
                if href2 not in list_link2 and href2 not in list_link1:
                    list_link2.append(href2)
                    print('**/*-добавляем ещё одну ссылку во второй список--', href2, list_link2)
                print('\n\nпроверка - начинается строка=====',i2.text.lower() , href2 , list_link1)
                if re.search('(.*персональных данных.*|.*политик.* .*конф.*|правила пользования сайтом|публичная оферта|конфиденциальность|.*политика обработки.*)', i2.text.lower()) and href2 not in list_link1:  # если есть такая формулировка открываем один раз, далее не идём
                    print('прямая ссылка2==содержатся точные слова с персом', href2, '/',i2.text,'+')
                    if re.search('(.*\.(pdf|PDF))', href2) or proverkapdf(href2)==1:  # если пдф файл - сохраняет - конвертирует в фото - конвертирует в текст - выдаёт текст
                        print('это пдф2, начинаю смотреть внутрь', href2)
                        destination2 = 'work_file.pdf'
                        url2 = href2
                        url2 = urllib.parse.quote(url2)
                        url2 = url2.replace('%3A', ':')
                        try:
                            urllib.request.urlretrieve(url2, destination2)
                            bad_pdf(url2)
                            print( '\nсохранил2 файл', url2, destination2)
                            text2 = esli_pdf('work_file.pdf')
                            print('просто текст2 из пдф2', text2[:5000])
                            save_anal = analizator("spar1.txt", "spar2.txt", text2)
                            print('текст2 из пдф2', save_anal, text2[:5000])
                            if save_anal[0] == 1:
                                tip_mat = 'pdf'
                                rezult.append({"название источника": url, "название страницы": re.sub(r"\s", " ", i2.text), "ссылка на страницу": href2, "тип источника": tip_mat, "отработавшие ключи": '\n'.join(save_anal[1])})
                                return print('найден пдф на втором уровне', href2, i2.text, url)
                        except:
                            pass
                    else:  # если будет найден сам словарь , то всё хватит , стоп
                        print(href2 )
                        text2 = re.sub(r"\s+", " ", BeautifulSoup(robot(href2), features="lxml").find('html').text)
                        print('не пдф - возможно, словарь прямо в тексте2 в этой ссылке2---  ', text2[:1000])
                        # анализ по сайту, используя словарь
                        save_anal = analizator("spar1.txt", "spar2.txt", text2)
                        if save_anal[0] == 1:
                            tip_mat = 'text'
                            rezult.append({"название источника": url, "название страницы": i2.text, "ссылка на страницу": href2, "тип источника": tip_mat, "отработавшие ключи": '\n'.join(save_anal[1])})
                            return print('найден текст на втором уровне', href2, i2.text, url)
    print('всё закончилось и не нашлось ничего', url)
    moneta=0
    slovar = orkrivalka_google(url)
    print('список найденных гуглом ссылок - ',slovar)
    for i in slovar:
        print(i, slovar[i])
        import sys
        if re.search('(.*персональных данных.*|.*политик.* .*конф.*|правила пользования сайтом|публичная оферта|конфиденциальность|.*политика обработки.*)', slovar[i]):  # если есть такая формулировка открываем один раз, далее не идём
            print('гугл ссылка  ==содержатся точные слова с персом', i, '-', slovar[i])



            if re.search('(.*\.(pdf|PDF))', i) or proverkapdf(i)==1:  # если пдф файл - сохраняет - конвертирует в фото - конвертирует в текст - выдаёт текст
                print('гугл пдф, начинаю смотреть внутрь', i)
                destination = 'work_file.pdf'
                url1 = i

                #url1 = urllib.parse.quote(url1, encoding='utf-8')
                print('урлиб ссылка', url1)
                url1 = url1.replace('%3A', ':')
                print('по этому адресу будет сейчас скачиваться пдф на комп', url1)
                try:
                    urllib.request.urlretrieve(url1, destination)
                    print('пробую скачать файл')
                    bad_pdf(url1)
                    print('\nгугл сохранил файл ')

                    text = esli_pdf('work_file.pdf')
                    save_anal = analizator("spar1.txt", "spar2.txt", text)
                    if save_anal[0] == 1:
                        tip_mat = 'pdf'
                        rezult.append({"название источника": url, "название страницы": re.sub(r"\s", " ", slovar[i]), "ссылка на страницу": i, "тип источника": tip_mat, "отработавшие ключи": '\n'.join(save_anal[1])})
                        print('гугл найден пдф ', i, slovar[i], url)
                        moneta = 1
                        break
                    else:
                        print('гугл не нашелся документ 1 уровень  - перейду к следующему-- ')
                except:
                    print('вышла ошибка в гугле пдф, буду бэд пдф пробовать')
                    print('имя ошибки = ',sys.exc_info())
                    znamya=bad_pdf_nosize(url1)
                    print('информация об исключении', traceback.print_exc())
                    if znamya==0:
                        print('\nгугл сохранил файл ')
                        text = esli_pdf('work_file.pdf')
                        save_anal = analizator("spar1.txt", "spar2.txt", text)
                        if save_anal[0] == 1:
                            tip_mat = 'pdf'
                            rezult.append({"название источника": url, "название страницы": re.sub(r"\s", " ", slovar[i]), "ссылка на страницу": i, "тип источника": tip_mat, "отработавшие ключи": '\n'.join(save_anal[1])})
                            print('гугл найден пдф искл ', i, slovar[i], url)
                            moneta = 1
                            break
                    else:
                        print('гугл не нашелся документ искл 1 уровень  - перейду к следующему-- ')
                    print('закончил бэд пдф искл ')
            else:  # если будет найден сам словарь , то всё хватит , стоп
                text = re.sub(r"\s+", " ", BeautifulSoup(robot(i), features="lxml").find('html').text)
                print('гугл не пдф в- возможно, прямо в тексте в этой ссылке1---  ', text[:1000])
                # анализ по сайту, используя словарь
                save_anal = analizator("spar1.txt", "spar2.txt", text)
                if save_anal[0] == 1:
                    tip_mat = 'text'
                    rezult.append({"название источника": url, "название страницы": re.sub(r"\s", " ", slovar[i]), "ссылка на страницу": i, "тип источника": tip_mat, "отработавшие ключи": '\n'.join(save_anal[1])})
                    print('найден текст на первом уровне', i, text, url)
                    moneta = 1
                    break

                else:
                    print('гугл не нашелся текст на странице   - переходим к следующему-- ')
    if moneta==0:
        print('в поиске гугла не найдено, программа завершается ')
        rezult.append({"название источника": url, "название страницы": '', "ссылка на страницу": '', "тип источника": '', "отработавшие ключи": ''})

startTime = time.time()
with open('links.txt', encoding='utf-8-sig') as f:
    list_links = f.read()
    list_links = list_links.split('\n')

for link in list_links:
    print('ссылка в работе- ',link, list_links.index(link)+1, len(list_links))
    otkrivalka(link)
    finish = pd.DataFrame(rezult)
    finish.columns = ["название источника", "название страницы", "ссылка на страницу", "тип источника", "отработавшие ключи"]
    finish.to_csv('table_found.csv', index=False)
    print(finish)
endTime = time.time() #время конца замера
totalTime = endTime- startTime
print("Время, затраченное на выполнение данного кода - ", totalTime, '\n', 'Количество ссылок -', len(list_links), '\n',
      'В среднем на одну ссылку секунд -', totalTime/len(list_links))

# otkrivalka('https://center-zalog.ru/')