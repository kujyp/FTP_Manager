from ftplib import FTP
import os
from .config import Parameter
from .src.ftptools import get_everyrelpath_fromftp
from .src.localtools import convert_path_sep
from .src import ftptools
from tqdm import tqdm
import sys
import unicodedata
import time


def uploadtoftp(PARAMS=None):
    # encoding for filename with korean ( for 2.7 )
    #reload(sys)
    #sys.setdefaultencoding('utf-8')

    # load config.py
    if PARAMS is None:
        PARMS = Parameter()

    ftp_domain = PARMS.ftp_domain
    ftp_user = PARMS.ftp_user
    ftp_pwd = PARMS.ftp_pwd
    ftp_homepath = PARMS.ftp_homepath
    ftp_targetpath = PARMS.ftp_targetpath
    ftp_uploadlocaldir = convert_path_sep(PARMS.ftp_uploadlocaldir)

    def load_allpath(path):
        res = []

        for root, dirs, files in os.walk(path):
            for file in files:
               filepath = os.path.join(root, file)
               #filepath = unicodedata.normalize('NFC', filepath)
               res.append(filepath)
        return res

    def file_exists_inftp(ftp_paths,filename):
        for ftp_path in ftp_paths:
            if ftp_path == filename:
                return True
        return False

    # ftp connect
    ftp = FTP(ftp_domain)
    ftp.encoding = "utf-8"
    ftp.login(ftp_user,ftp_pwd)
    print('Connected FTP Server : \t\t' + ftp_domain)

    # existing FTP files
    ftp_path = (ftp_homepath + '/' + ftp_targetpath)
    ftp_relpaths = get_everyrelpath_fromftp(ftp, ftp_path)
    print('Connected FTP Dir : \t\t' + ftp_path)

    local_paths = load_allpath(ftp_uploadlocaldir)
    local_abspathlen = len(ftp_uploadlocaldir)

    pbar = tqdm(local_paths)
    for local_path in pbar:
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
            pbar.set_description('Exist file : \t\t\t\t' + local_relpath) # todo exist korean file
        else:
            try:
                ftptools.mkdir_unless_exist(ftp, ftp_curpath)
                ftp.cwd(ftp_curpath)
                pbar.set_description('Uploading ... \t\t\t\t' + local_relpath)
                ftp.storbinary('STOR %s' % filename, local_file)
            except:
                pbar.set_description('Uploading ... \t\t\t\t' + local_relpath + ' retry . ')
                time.sleep(1)
                pbar.set_description('Uploading ... \t\t\t\t' + local_relpath + ' retry .. ')
                time.sleep(1)
                pbar.set_description('Uploading ... \t\t\t\t' + local_relpath + ' retry ... ')
                time.sleep(1)
                ftp.storbinary('STOR %s' % filename, local_file)

    ftp.quit()