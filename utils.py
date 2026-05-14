import os


def valid_file_name():
    files = os.listdir('./files')
    valid_files = []
    for file in files:
        if '.xlsx' in file and '~$' not in file:
            valid_files.append(file)
    return sorted(valid_files, key=lambda x: int(x.split('_G')[1].split('.')[0]))


if __name__ == '__main__':
    valid_files = valid_file_name()
    print(sorted(valid_files, key=lambda x: int(x.split('_G')[1].split('.')[0])))
