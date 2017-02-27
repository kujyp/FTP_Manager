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
ftp_downloadlocaldir = PARMS.ftp_downloadlocaldir

# mkdir in local
localdir = ftp_downloadlocaldir
try:
    os.stat(localdir)
except:
    os.mkdir(localdir)
    print('Make directory in local : \t' + localdir)

# ftp connect
ftp = FTP(ftp_domain)
ftp.login(ftp_user,ftp_pwd)
print('Connected FTP Server : \t\t' + ftp_domain)

path = (ftp_homepath + '/' + ftp_targetpath)
ftp.cwd(path)
print('Connected FTP Dir : \t\t' + path)

# Download all files
files = ftp.nlst()
for file in files:
    filename = file.split('/')[-1]

    localfilepath = os.path.join(localdir, filename)
    if os.path.exists(localfilepath):
        print('Exist file : \t\t\t\t' + localfilepath)
    else:
        print("Downloading ... \t\t\t" + filename)
        ftp.retrbinary('RETR %s' % filename, open(localfilepath, 'wb').write)

ftp.quit()
