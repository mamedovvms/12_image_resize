# Изменение размеров картики

Программа изменяет размер картинки.
В качестве параметров передается файл картинки и параметры изменения картинки.


# Описание

Параметр файла изображения - это обязательный параметр.
Не обязательные параметры ``--width - ширина, --height - высота, --scale - масштаб``\
Логика работы такая:
- Если указана только ширина – высота считается так, чтобы сохранить пропорции изображения. 
И наоборот. – Если указана и ширина и высота – создается именно такое изображение. 
Выводится в консоль предупреждение, если пропорции не совпадают с исходным изображением.
- Если указан масштаб, то ширина и высота указаны быть не могут. Иначе никакого ресайза не происходит
 и скрипт выводит соответстующую ошибку 
```bash
 $ python image_resize.py temp.jpg --width 100 --scale 2
Параметры ширина и высота не задаются с параметром масштаб
```
- Если не указан путь до финального файла, то результат кладётся рядом с исходным файлом.Например:

```bash
Если исходный файл называется pic.jpg (100x200), то после вызова python image_resize.py --scale 2 pic.jpg должен появиться файл pic__200x400.jpg.
```
Параметр ```scale > 0``` . Если параметр меньше 1, то размер изображения уменьшится.  
# Примеры
```bash
$ python image_resize.py temp.jpg --width 100 --height 50
Пропорции не сохранены
Измененное изображение temp__100x50.jpg

$ python image_resize.py temp.jpg --width 100
Измененное изображение temp__100x100.jpg

$ python image_resize.py temp.jpg  --scale 0.5
Измененное изображение temp__270x270.jpg
```

# Цель проекта

Код написан для образовательных целей. Учебный курс для веб-разработчиков - [DEVMAN.org](https://devman.org)