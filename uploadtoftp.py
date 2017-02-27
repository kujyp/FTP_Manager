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

def file_exists_inftp(ftpfiles,filename):
    for ftpfile in ftpfiles:
        if ftpfile == filename:
            return True
    return False

# ftp connect
ftp = FTP(ftp_domain)
ftp.login(ftp_user,ftp_pwd)
print('Connected FTP Server : \t\t' + ftp_domain)

path = (ftp_homepath + '/' + ftp_targetpath)
ftp.cwd(path)
print('Connected FTP Dir : \t\t' + path)

paths = load_allpath(ftp_uploadlocaldir)

# existing FTP files
ftpfilepaths = ftp.nlst()
ftpfiles = []
for ftpfilepath in ftpfilepaths:
    ftpfiles.append(ftpfilepath.split('/')[-1])

# FILEPATH windows(\) or mac(/)...
if paths[0].find('\\') == -1:
    spliter = '/'
else:
    spliter = '\\'

for path in paths:
    filename = path.split(spliter)[-1]
    file = open(path,'rb')

    if file_exists_inftp(ftpfiles,filename):
        print('Exist file : \t\t\t\t' + filename)
    else:
        print("Uploading ... \t\t\t\t" + filename)
        ftp.storbinary('STOR %s' % filename, file)

ftp.quit()