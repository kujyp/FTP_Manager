import os


def mkdir_unless_exist(local_path):
    dirs = local_path.split(os.sep)
    path = ''

    for dir in dirs:
        if dir == '':
            continue

        next_path = path + dir + os.sep
        try:
            os.stat(next_path)
        except:
            print('\nMake dir : \t\t\t\t\t' + next_path)
            os.mkdir(next_path)
        path = next_path

def convert_path_sep(local_path):
    return local_path.replace("/",os.sep)