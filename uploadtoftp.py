from ftplib import FTP
import os
from config import Parameter


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
        for dir in dirs:
            res += load_allpath(os.path.join(path,dir))
        for file in files:
            filepath = os.path.join(path, file)
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
ftp_fullpaths = ftp.nlst()
print(ftp_fullpaths)
ftp_paths = []
for ftp_fullpath in ftp_fullpaths:
    ftp_path = ftp_fullpath.split('/')[-1]
    ftp_paths.append(ftp_path)

for local_path in local_paths:
    filename = local_path.split(os.sep)[-1]

    # ignore .DS_Store
    if filename[0] == '.':
        continue

    local_file = open(local_path,'rb')

    if file_exists_inftp(ftp_paths,filename):
        print('Exist file : \t\t\t\t' + filename)
    else:
        print("Uploading ... \t\t\t\t" + filename)
        ftp.storbinary('STOR %s' % filename, file)

ftp.quit()