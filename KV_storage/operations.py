def execute_command(storage, raw_data):
    str_command, arg1, arg2 = parse_args(raw_data)
    try:
        command = COMMANDS[str_command]
    except KeyError:
        return 'Некорректный ввод\nКоманды не существет\nПопробуйте заново'
    else:
        return command(storage, arg1, arg2)


def parse_args(raw_data):
    raw_data = raw_data.split(maxsplit=2)
    command = raw_data[0]
    arg1 = None
    arg2 = None

    if len(raw_data) == 2:
        arg1 = raw_data[1]

    if len(raw_data) > 2:
        arg1 = raw_data[1]
        arg2 = raw_data[2]

    return command, arg1, arg2


def add(storage, key, data):
    storage.add(key, data)
    return 'Ключ добавлен'


def my_del(storage, key, arg):
    try:
        storage.delete(key)
        return 'Ключ удален'
    except KeyError:
        return 'Ключа не существует'


def get(storage, key, arg):
    try:
        return storage.get(key)
    except KeyError:
        return 'Ключа не существует'


def save_state(storage, arg1=None, arg2=None):
    storage.save()
    return 'состояние сохранено'


def load(storage, arg1=None, arg2=None):
    storage.load()
    return 'хранилище загружено'


COMMANDS = {
    'add': add,
    'del': my_del,
    'get': get,
    'save': save_state,
    'load': load
}
