import os


def valid_file_name():
    files = os.listdir('./files')
    valid_files = []
    for file in files:
        if '.xlsx' in file and '~$' not in file:
            valid_files.append(file)
    return valid_files


if __name__ == '__main__':
    valid_files = valid_file_name()
    print(valid_files)
