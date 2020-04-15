from external_sort import ext_sorting
import hashlib
import os


class TestExternalSort:
    def test_main(self):
        ext_sorting.main(1024, 'tests/example/in.txt', 'tests/example/out.txt')
        assert get_hash_md5('tests/example/out.txt') == get_hash_md5('tests/example/ideal/out.txt')

    def test_sort_big_file(self):
        ext_sorting.main(10, 'tests/example/big_in.txt', 'tests/example/big_out.txt')
        ideal_hash = get_hash_md5('tests/example/big_out.txt')
        res_hash = get_hash_md5('tests/example/ideal/ex_res.txt')
        assert ideal_hash == res_hash

    def test_write_in_tmp_file(self):
        strings = [b'hi', b'nice to see you', b'bye']
        ext_sorting.write_in_tmp_file(strings, 2)
        assert os.path.exists('tests/temp/2')


def get_hash_md5(filename):
    with open(filename, 'rb') as f:
        m = hashlib.md5()
        while True:
            data = f.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()
