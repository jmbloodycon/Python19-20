import argparse


def create_parser():
    parser = argparse.ArgumentParser(description="EXTERNAL SORTING")
    parser.add_argument('buffer_size', type=int, default=None, help="Размер памяти в килобайтах")
    parser.add_argument('file_path', type=str, default=None, help="Путь до файла, который нужно отсортить")
    parser.add_argument('out_file_path', type=str, default=None, help="Путь до файла с результатом")
    return parser
