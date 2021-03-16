# reMarkable2_backup

Currently just a simple module used to backup reMarkable2 to a tar.gz file over USB using SFTP / SSH.

Initial run takes about 3-4 minutes to download files and 1-2 minutes for tar.gz creation. This portion will eventually have a progress bar but for now it will state "Download started" & "Starting creation of archive" when reporting progress.

Canceling and restarting will report directories already exist exceptions in /tmp paths but will re-download everything.

Eventual refactoring will feature 3 parts. CLI, TUI & GUI to test out some features using different frameworks.

## Installation

Clone repo and cd to "cli" directory.

Make sure the reMarkable2 tablet is connected and screen is not sleeping.

```bash
git clone https://github.com/mzaran/reMarkable2_backup.git
cd reMarkable2_backup/cli/
./backup.py
```

## Usage

### Over ride defaults
Default run of backup.py will use the default values set in the class constructor. (__init__)

The defaults depend on a SSH key to access Remarkable as shown https://remarkablewiki.com/tech/ssh under "Tips" -> "Setting up ssh-keys"

To force password use please modify line 10 for entry "password=None" to a string value as shown.

```python
    def __init__(self, remote_path, destination, host='10.11.99.1', port=22, username='root', password='password_goes_here', log='./paramiko.log'):
```

### File locations
Leave the first path alone since this will be the data on the reMarkable2 tablet. 

If you want to specify a different location for the backup's to be stored please change './backup/' to the path you require.

```python
line 102 / 103 
create_backup = RemarkableBackup('/home/root/.local/share/remarkable/xochitl/', './backup/')
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
