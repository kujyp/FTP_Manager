from ftplib import FTP
import os
from config import Parameter
from src.ftptools import get_everypath_fromftp, mkdir_unless_exist


# load config.py
PARMS = Parameter()
ftp_domain = PARMS.ftp_domain
ftp_user = PARMS.ftp_user
ftp_pwd = PARMS.ftp_pwd
ftp_homepath = PARMS.ftp_homepath
ftp_targetpath = PARMS.ftp_targetpath
ftp_uploadlocaldir = PARMS.ftp_uploadlocaldir

def load_allpath(path):
    res = []

    for root, dirs, files in os.walk(path):
        for file in files:
           filepath = os.path.join(root, file)
           res.append(filepath)
    return res

def file_exists_inftp(ftp_paths,filename):
    for ftp_path in ftp_paths:
        if ftp_path == filename:
            return True
    return False

# ftp connect
ftp = FTP(ftp_domain)
ftp.login(ftp_user,ftp_pwd)
print('Connected FTP Server : \t\t' + ftp_domain)

ftp_path = (ftp_homepath + '/' + ftp_targetpath)
ftp.cwd(ftp_path)
print('Connected FTP Dir : \t\t' + ftp_path)

local_paths = load_allpath(ftp_uploadlocaldir)

# existing FTP files
ftp_fullpaths = get_everypath_fromftp(ftp, '')
#print(ftp_fullpaths)

ftp_relpaths = []
ftp_abspathlen = len(ftp_path)
for ftp_fullpath in ftp_fullpaths:
    ftp_relpath = ftp_fullpath[ftp_abspathlen:]
    ftp_relpaths.append(ftp_relpath)
    # print(ftp_relpath)

local_abspathlen = len(ftp_uploadlocaldir)
for local_path in local_paths:
    filename = local_path.split(os.sep)[-1]
    dirnames = local_path.split(os.sep)[1:-1]

    ftp_curpath = ftp_path
    for dirname in dirnames:
        ftp_curpath= ftp_curpath + '/' + dirname

    # ignore .DS_Store
    if filename[0] == '.':
        continue

    local_file = open(local_path,'rb')
    local_relpath = local_path[local_abspathlen:]

    if file_exists_inftp(ftp_relpaths,local_relpath):
        print('Exist file : \t\t\t\t' + local_relpath)
    else:
        mkdir_unless_exist(ftp, ftp_curpath)
        ftp.cwd(ftp_curpath)
        #ftp.pwd()
        print("Uploading ... \t\t\t\t" + local_relpath)
        ftp.storbinary('STOR %s' % filename, local_file)

ftp.quit()