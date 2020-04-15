from external_sort import argparser


def test_parse_args():
    parser = argparser.create_parser()
    args = parser.parse_args(['3', 'lol', 'kek'])
    assert args.buffer_size == 3
