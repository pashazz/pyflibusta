# PyFlibusta
<b>PyFlibusta</b> - это поисковик по базе библиотеки <a href=http://flibusta.net> Flibusta </a>
Для его использования вам необходимо скачать зеркало библиотеки из zip-файлов отсюда: <a href=http://booktracker.org/viewtopic.php?t=46979>Книжный трекер</a>

## Каталог
Программе необходим каталог Флибусты, который находится по адресу  http://www.flibusta.net/catalog/catalog.zip

## Запуск
    chmod +x flibusta.py
    ./flibusta.py -h #получение помощи
    
## Требования к системе
Python 3 должен быть установлен в $PATH

## Пример запроса (см. справку по опциям)
    ./flibusta.py -c test/catalog.txt -ln 'Толстой' -t 'Война и мир' -x ~/Документы -d ~/media/books/Флибуста
    
Данный запрос скопирует все книги романа "Война и мир" Л. Толстого, отмеченные в каталоге test/catalog.txt, имеющиеся в коллекции  ~/media/books/Флибуста
