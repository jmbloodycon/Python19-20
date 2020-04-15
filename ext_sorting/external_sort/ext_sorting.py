from external_sort import argparser
import os
import os.path
import shutil
import heapq


def sort(out_file):
    temp_files = []

    for file in os.listdir('temp'):
        temp_files.append(open('temp/{}'.format(file)))
    out = heapq.merge(*temp_files)
    with open(out_file, 'w') as result_file:
        for line in out:
            result_file.write(line)

    for file in temp_files:
        file.close()


def make_temp_files(file_path, buffer_size):
    temp_file_counter = 0
    buffer_size *= 1024
    current_size = 0

    with open(file_path) as file:
        temp_file_strings = []
        file_line = file.readline().encode()

        while file_line != b'':
            current_size += len(file_line)
            temp_file_strings.append(file_line)

            if current_size >= buffer_size:
                current_file_strings = temp_file_strings[:-1]
                write_in_tmp_file(current_file_strings, temp_file_counter)
                temp_file_counter += 1
                current_size = len(temp_file_strings[-1])
                temp_file_strings = [temp_file_strings[-1]]

            file_line = file.readline().encode()

        write_in_tmp_file(temp_file_strings, temp_file_counter)


def write_in_tmp_file(temp_file_strings, temp_file_counter):
    with open('temp/{}'.format(temp_file_counter), 'w') as temp_file:
        temp_file_strings.sort()
        for line in temp_file_strings:
            temp_file.write(line.decode())


def main(buffer_size, file_path, out_file):
    if os.path.exists('temp'):
        shutil.rmtree('temp')
    os.mkdir('temp')

    make_temp_files(file_path, buffer_size)
    sort(out_file)


def start():
    args = argparser.create_parser().parse_args()
    main(args.buffer_size, args.file_path, args.out_file_path)


if __name__ == "__main__":
    start()
