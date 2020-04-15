# Image Resizer

#### Требования
Python версии не ниже 3.7

#### Описание
Функции API:
Принимает get и post запросы

GET:

    /task/<string:tasks_id>
    /image/<string:images_id>

POST:

    /task

#### Пример запуска:     
    make up

#### Как работать 
1 `make venv` - дополнительные зависимости

2 `make test` - запуск тестов

3 `make format lint` - прохождение линтеров
    
##### Используемые библиотеки
* `flask`
* `typing`
* `redis`
* `os.path`
* `rq`
* `pillow`
* `base64`

### Тесты
> Покрытие тестами более 90%

![Game](img/test.jpg)



### Build service:
	make build
