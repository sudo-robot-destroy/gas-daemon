# gas-daemon
A daemon for running git-auto-sync since termux doesn't use systemd

ChatGPT guidance: 

Got it! Let's focus on using Daemoniker to create a cross-platform Python script that can run as a daemon in Ubuntu, Termux, and Windows without relying on systemd. Here’s a step-by-step guide that covers all three environments.

Step 1: Install Required Packages
For Ubuntu
Open your terminal and run the following commands to install necessary packages:

bash
```
sudo apt update
sudo apt install python3-pip
pip3 install python-daemoniker watchdog schedule
```
For Termux
Open Termux and run the following commands:

bash
```
pkg update
pkg install python
pip install python-daemoniker watchdog schedule
```
For Windows
Make sure you have Python installed. You can download it from the official Python website.
Open Command Prompt (cmd) and run:
bash
```
pip install python-daemoniker watchdog schedule
```
Step 2: Create Your Python Script
Create a Python script (e.g., git_sync_daemon.py) using a text editor (e.g., nano for Ubuntu and Termux or Notepad for Windows).

Example Code
Here’s the code to include in git_sync_daemon.py:

python
```
import time
import schedule
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from daemoniker import Daemon
import configparser
import os

class MyEventHandler(FileSystemEventHandler):
    def __init__(self, directory):
        self.directory = directory
        
    def on_modified(self, event):
        if not event.is_directory:  # Ignore directory changes
            print(f'{event.src_path} has been modified. Running git-auto-sync.')
            self.run_git_auto_sync()

    def run_git_auto_sync(self):
        # Change the working directory and run the command
        subprocess.run(["git-auto-sync", "sync"], cwd=self.directory, check=True)

def job(directory):
    print("Running scheduled git-auto-sync...")
    subprocess.run(["git-auto-sync", "sync"], cwd=directory, check=True)

def run_daemon(directory, interval):
    # Set up file system monitoring
    event_handler = MyEventHandler(directory)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()

    # Schedule the job to run every interval minutes
    schedule.every(interval).minutes.do(lambda: job(directory))

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    # Read the config file
    config = configparser.ConfigParser()
    config.read('config.ini')

    directory = config['settings']['directory']
    interval = int(config['settings']['schedule_interval'])

    daemon = Daemon(lambda: run_daemon(directory, interval))
    daemon.start()
```
Step 3: Make the config file: 
Create a configuration file named config.ini with the following content:

ini
```
[settings]
directory = /path/to/your/directory
schedule_interval = 10  # in minutes
```

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
Summary
Install the necessary packages for your environment.
Create the Python script using Daemoniker to monitor a directory and execute git-auto-sync sync.
Run the script as a daemon in Ubuntu, Termux, or Windows, using appropriate methods for each environment.
Monitor the output to ensure it’s functioning as expected.
This setup allows your script to run continuously as a daemon, handling file modifications and scheduled tasks without relying on systemd or Docker. If you have any further questions or need assistance with specific parts, feel free to ask!
