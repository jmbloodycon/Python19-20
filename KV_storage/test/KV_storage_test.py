import unittest
import operations as m
from Storage import Storage


class KVStorageTests(unittest.TestCase):
    def test_parse_args(self):
        result = m.parse_args('lol kek cheburek')
        self.assertEquals(result, ('lol', 'kek', 'cheburek'))

    def test_parse_args_with_one_arg(self):
        result = m.parse_args('lol kek')
        self.assertEquals(result, ('lol', 'kek', None))

    def test_parse_args_with_spaces_in_second_arg(self):
        result = m.parse_args('lol kek cheburek hehe')
        self.assertEquals(result, ('lol', 'kek', 'cheburek hehe'))

    def test_add(self):
        result = m.add(Storage(), 'lol', 'kek')
        self.assertEquals(result, 'Ключ добавлен')

    def test_dell(self):
        storage = Storage()
        m.add(storage, 'lol', 'kek')
        result = m.my_del(storage, 'lol', None)
        self.assertEquals(result, 'Ключ удален')

    def test_dell_with_exception(self):
        storage = Storage()
        m.add(storage, 'lol', 'kek')
        result = m.my_del(storage, 'lel', None)
        self.assertEquals(result, 'Ключа не существует')

    def test_get(self):
        storage = Storage()
        m.add(storage, 'lol', 'kek')
        result = m.get(storage, 'lol', None)
        self.assertEquals(result, 'kek')

    def test_get_with_exception(self):
        storage = Storage()
        m.add(storage, 'lol', 'kek')
        result = m.get(storage, 'lel', None)
        self.assertEquals(result, 'Ключа не существует')

    def test_execute_command_not_found(self):
        storage = Storage()
        result = m.execute_command(storage, 'lol')
        expected = 'Некорректный ввод\nКоманды не существет\nПопробуйте заново'
        self.assertEquals(result, expected)

    def test_execute_command(self):
        storage = Storage()
        result = m.execute_command(storage, 'add lol kek')
        self.assertEquals(result, 'Ключ добавлен')

    def test_save_state(self):
        storage = Storage()
        result = m.save_state(storage)
        self.assertEquals(result, 'состояние сохранено')

    def test_load(self):
        storage = Storage()
        result = m.load(storage)
        self.assertEquals(result, 'хранилище загружено')
