import click
import shutil
import paramiko
import os
import tarfile
import time
from stat import S_ISDIR, S_ISREG


class RemarkableBackup:
    def __init__(self, remote_path, destination, host='10.11.99.1', port=22, username='root', password=None, log='./paramiko.log'):
        self.remote_path = remote_path
        self.destination = destination
        self.temp = '/tmp/remarkable2_' + time.strftime('%m%d%Y') + '/'
        self.log = log
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        paramiko.util.log_to_file(self.log)
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if password is not None:
            self.client.connect(hostname=self.host, port=self.port,
                                username=self.username, password=self.password)
        else:
            self.client.connect(hostname=self.host,
                                port=self.port, username=self.username)

        self.sftp = self.client.open_sftp()

    def scan_files(self, remote_dir):
        '''
        scan remarkable2 for files -> creates list
        '''
        return [file.filename for file in self.sftp.listdir_iter(remote_dir) if S_ISREG(file.st_mode)]

    def download_files(self, remote_dir, temp_destination):
        '''
        uses sftp to download files 1 by 1 from remarkable2
        '''
        return [self.sftp.get(remote_dir + file, temp_destination + file) for file in self.scan_files(remote_dir)]

    def scan_directories(self, remote_dir):
        '''
        scan remarkable2 for directories -> creates list
        '''
        return [file_indir for file_indir in self.sftp.listdir_iter(remote_dir) if S_ISDIR(file_indir.st_mode)]

# SPLIT THIS BETWEEN CREATE DIRECTORIES & GET DIRS?
    def create_directories(self, remote_dir):
        '''
        locate directories and create in local path
        '''
        for directory in self.scan_directories(remote_dir):
            value = oct(directory.st_mode)
            dir_perms = int(str(value[4:]), 8)
            os.mkdir(self.temp + directory.filename, mode=dir_perms)
            self.download_files(remote_dir + directory.filename +
                                '/', self.temp + directory.filename + '/')

    def backup_compress(self):
        '''
        gzip stuff goes here
        '''
        with tarfile.open(self.destination + 'remarkable_2_' + time.strftime('%m%d%Y') + '.tar.gz', 'w:gz') as tar:
            for name in os.listdir(self.temp):
                tar.add(self.temp + name)
            tar.close()

    def directory_cleanup(self):
        '''
        delete tmp directory and files after backup and tar.gz creation
        '''
        try:
            shutil.rmtree(self.temp)
        except Exception as e:
            raise e

    def full_backup(self):
        '''
        triggers full backup methods in correct order
        first attempts to make temp directory
        '''
        try:
            os.mkdir(self.temp)
        except FileExistsError as e:
            print(e, 'Looks like temp backup directory exists overwriting files...')

        print('Download started')
        self.download_files(self.remote_path, self.temp)
        self.create_directories(self.remote_path)
        self.sftp.close()
        print('Starting creation of archive')
        self.backup_compress()
        self.directory_cleanup()


if __name__ == '__main__':
    try:
        create_backup = RemarkableBackup(
            '/home/root/.local/share/remarkable/xochitl/', './testing_dump/')
        create_backup.full_backup()
        print('Backup complete')
    except Exception as e:
        raise e
