# gas-daemon
A daemon for running git-auto-sync since termux doesn't use systemd

## Installation:  
Make sure git-auto-sync is installed and added to path. 
Install watchdog, schedule, and daemoniker using pip. 
```
pip install python-daemoniker watchdog schedule
```
## Configuration:  
You need a config.ini file in the same directory as gas-daemon.py that looks like this: 
```
[settings]
directory = c:\Users\8to\Desktop\org-repo
schedule_interval = 10
```


## TODO notes below here
For Windows, use double backslashes or raw string format for paths (e.g., r"C:\\path\\to\\your\\directory").
Step 4: Run Your Script as a Daemon
For Ubuntu and Termux
Run the script directly in the terminal:
bash
```
python3 git_sync_daemon.py
```
Note: In Termux, simply use python instead of python3.

To run it in the background, you can use:
bash
```
nohup python3 git_sync_daemon.py &
```
This will keep your script running even after you close the terminal.

For Windows
Open Command Prompt and navigate to the directory where your script is located.

Run the script:

cmd
```
python git_sync_daemon.py
```
To run it in the background, you can use a batch file. Create a .bat file (e.g., run_git_sync.bat) with the following content:

batch
```
@echo off
start /b python git_sync_daemon.py
```
Step 5: Monitoring Output
For Ubuntu and Termux: The output will be displayed in the terminal or saved in nohup.out if you used nohup.

For Windows: The output will be displayed in the Command Prompt. If you want to log output to a file, you can modify the .bat file:

batch
```
@echo off
start /b python git_sync_daemon.py >> output.log 2>&1
```
