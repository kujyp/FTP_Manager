from ftplib import FTP
import os
from .config import Parameter
from .src.ftptools import get_everyrelpath_fromftp
from .src.localtools import convert_path_sep
from .src import localtools
from tqdm import tqdm
import sys
import time


def downloadfromftp(PARMS=None):
    # encoding for filename with korean ( for 2.7 )
    #reload(sys)
    #sys.setdefaultencoding('utf-8')

    # load config.py
    if PARMS is None:
        PARMS = Parameter()

    ftp_domain = PARMS.ftp_domain
    ftp_user = PARMS.ftp_user
    ftp_pwd = PARMS.ftp_pwd
    ftp_homepath = PARMS.ftp_homepath
    ftp_targetpath = PARMS.ftp_targetpath
    ftp_downloadlocaldir = convert_path_sep(PARMS.ftp_downloadlocaldir)

    # mkdir in local
    local_dir = ftp_downloadlocaldir
    localtools.mkdir_unless_exist(ftp_downloadlocaldir)

    # ftp connect
    ftp = FTP(ftp_domain)
    print('Connecting FTP Server : \t\t' + ftp_domain)
    ftp.encoding = "utf-8"
    ftp.login(ftp_user,ftp_pwd)

    ftp_path = (ftp_homepath + '/' + ftp_targetpath)
    print('Connecting FTP Dir : \t\t' + ftp_path)
    ftp_relpaths = get_everyrelpath_fromftp(ftp, ftp_path)

    # Download all files
    pbar = tqdm(ftp_relpaths)
    for ftp_relpath in pbar:
        filename = ftp_relpath.split('/')[-1]
        dirnames = ftp_relpath.split('/')[1:-1]

        ftp_curpath = ftp_path
        local_path = local_dir
        for dirname in dirnames:
            ftp_curpath = ftp_curpath + '/' + dirname
            local_path = os.path.join(local_path, dirname)

        local_pathwithfilename = os.path.join(local_path, filename)
        if os.path.isfile(local_pathwithfilename):
            pbar.set_description('Exist file : \t\t\t\t' + local_pathwithfilename)
        else:
            try:
                localtools.mkdir_unless_exist(local_path)
                ftp.cwd(ftp_curpath)
                pbar.set_description("Downloading ... \t\t\t" + local_pathwithfilename)
                ftp.retrbinary('RETR %s' % filename, open(local_pathwithfilename, 'wb').write)
            except:
                pbar.set_description("Downloading ... \t\t\t" + local_pathwithfilename + ' retry . ')
                time.sleep(1)
                pbar.set_description("Downloading ... \t\t\t" + local_pathwithfilename + ' retry .. ')
                time.sleep(1)
                pbar.set_description("Downloading ... \t\t\t" + local_pathwithfilename + ' retry ... ')
                time.sleep(1)
                ftp.retrbinary('RETR %s' % filename, open(local_pathwithfilename, 'wb').write)

    ftp.quit()
