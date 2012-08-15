#!/usr/bin/env python3
'''
Для получения помощи наберите ./flibusta.py -h
(c) Pavel Borisov (http://github.com/pashazz) 2012.
Незаконно в некоторых странах
Распространяется под лицензией GNU GPL 3 или более поздней
'''

import argparse, sys, glob, zipfile, os
from flibusta import catalog


def show(directory, iterable, quiet, extract, limit, format):
    '''
    показывает информацию о книге (iterable - список книг, отдаваемый searchCatalog)
    directory - папка с архивами
    '''
    if not iterable:
        print ('{prog}: по данному запросу ничего не найдено'.format(prog=sys.argv[0]), file=sys.stderr)
        
    if not format:
        format = '{firstname} {lastname}  - {title}'
    info = \
    '''
    {title}
    
    Серия: {series}
    Подзаголовок: {subtitle}
    Автор: {lastname}, {firstname} {middlename}
    Язык: {language}
    Год выпуска: {year}
    ID книги: {id}
    Файл: {file} в архиве {archive}
    '''
    #if isinstance(extract, str) and (not os.path.exists(extract)):
    #    os.mkdir(extract)
    
    i = 0
    if extract:
        if not os.path.exists(extract):
            os.mkdir(extract)
        os.chdir(extract)
        
    for dct in iterable:
        if limit >= 0  and i >= limit:
            return 
        
        archive, file = catalog.findFile(dct['id'], directory)
        if not quiet:
            print(info.format(archive=archive, file=file, **dct))
            print()
            print()
        if extract:
            myzip = zipfile.ZipFile(archive)
            myzip.extract(file)
            os.rename(file, '.'.join(format.format(**dct), os.path.splitext(file)[1]))
            
        i += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Сканер локальной копии библиотеки Flibusta',
                                     epilog='''Библиотеку можно загрузить здесь: http://book.libertorrent.com/viewforum.php?f=245,
                                             а каталог здесь: http://www.flibusta.net/catalog/catalog.zip
                                            
                                        '''
                                     )
    parser.add_argument('-q', '--quiet', help='Не печатать ничего. Используйте с -x', action='store_true')
    parser.add_argument('-c', '--catalog', help='Каталог библиотеки Флибуста (обычно catalog.txt)', default='catalog.txt', metavar='ФАЙЛ КАТАЛОГА')
    parser.add_argument('-n', '--limit', metavar='ЛИМИТ', help='Количество книг для вывода', type=int, default= -1)
    act_gr = parser.add_argument_group('Действия')
    parser.add_argument('-f', '--format', metavar='ФОРМАТ', help='Формат выходных файлов')
       
    parser.add_argument('-d', '--directory', help='Директория с архивом библиотеки', required=True, metavar='ДИРЕКТОРИЯ')
    parser.add_argument('-x', '--extract', help='Распаковать файлы автоматически в директорию (по умолчанию в рабочую)', metavar='ДИРЕКТОРИЯ',
                        default=False, const=os.getcwd(), nargs='?'
                        )  
    reg = parser.add_argument_group('Поля поиска с помощью регулярных выражений')
    reg.add_argument('-t', '--title', help='Название книги', metavar='НАЗВАНИЕ')
    reg.add_argument('-fn', '--firstname', help='Имя автора', metavar='ИМЯ')
    reg.add_argument('-mn', '--middlename', help='Отчество автора', metavar='ОТЧЕСТВО')
    reg.add_argument('-ln', '--lastname', help='Фамилия автора', metavar='ФАМИЛИЯ')
    reg.add_argument('-st', '--subtitle', help='Подзаголовок книги', metavar='ПОДЗАГОЛОВОК')
    reg.add_argument('-s', '--series', help='Серия', metavar='СЕРИЯ')
    reg.add_argument('-l', '--language', help='Язык книги (двухбуквенный формат)', metavar='ЯЗЫК')
    reg.add_argument('-y', '--year', help='Год выхода книги', metavar='ГОД')
    
    
    mut_gr = parser.add_mutually_exclusive_group()
    mut_gr.add_argument('-i', '--id', help='ID книги для точного поиска', type=int)
    mut_gr.add_argument_group(reg)
    
    args = parser.parse_args()
    
    if  not glob.glob1(args.directory, '*.zip'):
        print('Не найдены архивы, выход')
        exit()
    
    if args.id:
        kwargs = {'id':args.id}
    else:
        varargs = vars(args)
        kwargs = dict()
        
        for key in catalog.keys:
            if key in varargs and varargs[key] is not None:
                kwargs[key] = varargs[key]
    
    genexp = catalog.searchCatalog(args.catalog, **kwargs)
    show (args.directory, genexp, args.quiet, args.extract, args.limit, args.format)
    
