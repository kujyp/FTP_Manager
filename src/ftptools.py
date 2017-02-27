from ftplib import error_perm

def get_everypath_fromftp(ftp, path):
    ftp.cwd(path)
    ftp.pwd()

    ftp_paths = ftp.nlst()

    everypath = []
    for ftp_path in ftp_paths:
        try:
            dir_flag = False
            ftp.cwd(ftp_path + "/")
            dir_flag = True
            everypath += get_everypath_fromftp(ftp, ftp_path + "/")
        except error_perm:
            if not dir_flag:
                everypath.append(ftp_path)
                #print ftp_path
    return everypath

def mkdir_unless_exist(ftp, ftp_curpath):
    dirs = ftp_curpath.split('/')
    path = '/'
    for dir in dirs:
        if dir == '':
            continue

        next_path = path + dir + '/'
        try:
            ftp.cwd(next_path)
        except error_perm:
            print('Make dir : \t\t\t\t' + next_path)
            ftp.mkd(dir)
        path = next_path