from ftplib import FTP
import os
from config import Parameter
from src.ftptools import get_everyrelpath_fromftp
from src import localtools

# load config.py
PARMS = Parameter()
ftp_domain = PARMS.ftp_domain
ftp_user = PARMS.ftp_user
ftp_pwd = PARMS.ftp_pwd
ftp_homepath = PARMS.ftp_homepath
ftp_targetpath = PARMS.ftp_targetpath
ftp_downloadlocaldir = PARMS.ftp_downloadlocaldir

# mkdir in local
local_dir = ftp_downloadlocaldir
localtools.mkdir_unless_exist(ftp_downloadlocaldir)

# ftp connect
ftp = FTP(ftp_domain)
ftp.login(ftp_user,ftp_pwd)
print('Connected FTP Server : \t\t' + ftp_domain)

ftp_path = (ftp_homepath + '/' + ftp_targetpath)
ftp_relpaths = get_everyrelpath_fromftp(ftp, ftp_path)
print('Connected FTP Dir : \t\t' + ftp_path)

# Download all files
for ftp_relpath in ftp_relpaths:
    filename = ftp_relpath.split('/')[-1]
    dirnames = ftp_relpath.split('/')[1:-1]

    ftp_curpath = ftp_path
    local_path = local_dir
    for dirname in dirnames:
        ftp_curpath = ftp_curpath + '/' + dirname
        local_path = os.path.join(local_path, dirname)

    local_pathwithfilename = os.path.join(local_path, filename)
    if os.path.isfile(local_pathwithfilename):
        print('Exist file : \t\t\t\t' + local_pathwithfilename)
    else:
        localtools.mkdir_unless_exist(local_path)
        ftp.cwd(ftp_curpath)
        print("Downloading ... \t\t\t" + local_pathwithfilename)
        ftp.retrbinary('RETR %s' % filename, open(local_pathwithfilename, 'wb').write)

ftp.quit()
