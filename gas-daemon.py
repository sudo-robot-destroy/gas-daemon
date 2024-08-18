import time
import schedule
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import configparser
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    # filename="gas_daemon.log",
    # encoding="utf-8",
    # filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)

class MyEventHandler(FileSystemEventHandler):
    def __init__(self, directory):
        self.directory = directory
        self.debounce_start = time.time()  # don't call sync more than once a second
        # Go ahead and sync as soon as you start
        logging.info("Running sync on start up")
        job(self.directory)

    def on_modified(self, event):
        if not event.is_directory and not self.is_hidden(event.src_path):  # Ignore directory changes and files in hidden folders
            logging.info(f'{event.src_path} has been modified. calling callback.')
            self.run_git_auto_sync()

    def run_git_auto_sync(self):
        debounce_end = time.time()
        if debounce_end - self.debounce_start > 5:
            self.debounce_start = time.time()
            job(self.directory)
        else:
            logging.info("Not syncing again - synced within last 5 seconds")

    def is_hidden(self, path):
        """Says if a path contains a hidden folder"""
        return any(part.startswith('.') for part in path.split(os.sep))
        return False

def job(directory):
    logging.info("Running git-auto-sync...")
    try:
        result = subprocess.run(
            ["git-auto-sync", "sync"],
            cwd=directory,
            capture_output=True,
            text=True,
            check=True)
        logging.info("git-auto-sync is complete")
    except subprocess.CalledProcessError as e:
        logging.error(
            "Something is wrong, maybe there is not internet available? \n"
            "We'll keep running and try again later\n\n"
            f"{e} \n\n"
            f"{e.stderr}"
        )


def run_daemon(directory, interval):
    # Set up file system monitoring
    event_handler = MyEventHandler(directory)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.event_queue.empty
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
    run_daemon(directory, interval)
