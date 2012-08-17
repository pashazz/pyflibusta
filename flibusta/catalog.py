'''
Functions to work with Flibusta's catalog
'''
keys = ('lastname', 'firstname', 'middlename', 'title', 'subtitle', 'language', 'year', 'series', 'id')

import re, glob, zipfile, os

import logging
logger = logging.getLogger(__name__)
hdlr = logging.FileHandler('flibusta.log')
frm = logging.Formatter('''%(asctime)s - %(name)s - %(levelname)s - %(message)s''')
hdlr.setLevel(logging.WARNING)
logger.setLevel(logging.DEBUG)
hdlr.setFormatter(frm)
logger.addHandler(hdlr)

def readCatalog(fileName):
    '''Читаем каталог флибусты 
    Первая строка каталога - список ключей словаря'''
    if not os.path.exists(fileName):
        print ('Нет такого файла: {} (рабочая директория ) {}'.format(fileName, os.getcwd()))
        raise IOError()
    
    
    global keys
    with open(fileName, 'rt') as cat:
        cat.readline() #пропуск первой строки
        
        for line in cat:
            book = dict(zip(keys, line.split(';')))
            try:
                book['id'] = int(book['id'])
            except:
                logger.warning ('readCatalog: {fn}:поле ID: {id} не похоже на int: оставляю как есть. Пожалуйста, исправьте каталог' \
                                .format(id=book['id'], fn=fileName))
                
            yield book
            
def searchCatalog(fileName, **kwargs):
    '''Ищем в каталоге по параметрам kwargs с использованием ф-ции re.search
    параметры в глобальной переменной keys'''
    for book in readCatalog(fileName):
        tests = []
        if 'id' in kwargs:
            if kwargs['id'] == book['id']:
                yield book
                continue
            else:
                continue
            
            
        for key in kwargs:
            tests.append(re.search(kwargs[key], book[key]))
        
        if all(tests):
            yield book
            

def processArchive(zipFile):
    '''выводим список файлов zip-архива'''
    try:
        file = zipfile.ZipFile(zipFile)
        return file.namelist()
    except:
        return []


def findFile(ID, directory):
    '''
    Пытаемся найти файл "id" в данной директории в одном из zip-файлов
    (так распространяется архив Flibusta)
    возвращаем кортеж: (полный путь к zip-архиву,название файла книги) Поддержка дубликатов не предусмотрена.
    
    '''
    if not isinstance(ID, int):
        raise TypeError('book ID is not int')
    for archive in glob.glob(directory + '/*.zip'):
        logger.info('processing file {}'.format(archive))
        for book in  processArchive(archive):
            #logging.info('processing book {}'.format(os.path.basename(book)))
            try:
                base = int(os.path.splitext(os.path.basename(book))[0])
            except:
                continue
            
            if base == ID:
                return archive, book
            
            
    return None, None
