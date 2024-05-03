import time
import boto3 #interacting with s3
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler #monitoring file system events

local_folder = 'D:\\SLIIT\\test3'
s3_bucket_name = 'testminindu'

s3 = boto3.client('s3')

class S3SyncHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return
        file_path = event.src_path
        # Sync file to S3 bucket
        s3.upload_file(file_path, s3_bucket_name, file_path[len(local_folder) + 1:])

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(S3SyncHandler(), local_folder, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
