# Проект "Vice Versa"
Реализация тестирования проектов YaNote и YaNews на unittest и pytest соответственно.

Проект является учебным. Основная польза в приобретении понимания реализации unittest и pytest тестов в проектах, с использованием:
- созданного общего ядра для unittest, с применением namedtuple для упакавки путей и использования их во всех тестах;
- созданных сложных фикстур для pytest, с применением namedtuple для упаковки разных категорий путей, для разных тестов;
- сложной реализации через namedtuple позволяющая куда лучше понять работу кортежей в Python.

## Развёртывание проекта:
+ Клонировать репозиторий и перейти в него в командной строке:
```shell script
git clone git@github.com:Romaizega/django_testing.git
```

```shell script
cd django_testing/
```

+ Cоздать и активировать виртуальное окружение (Windows/Bash):
```shell script
python -m venv venv
```

```shell script
source venv/Scripts/activate
```

+ Установить зависимости из файла requirements.txt:
```shell script
python -m pip install --upgrade pip
```

```shell script
pip install -r requirements.txt
```

<br>

## Тестирование проекта:
### Unittest
+ Перейти в директорию проекта `ya_note`:
```shell script
cd ya_note/
```
+ Запустить тесты:
```shell script
python manage.py test
```

### Pytest
+ Перейти в директорию проекта `ya_news`:
```shell script
cd ya_news/
```
+ Запустить тесты:
```shell script
pytest
```
