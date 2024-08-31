import os
import time
import logging
import boto3  #interacting with s3
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler #monitoring file system events

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Local directory to monitor
local_folder = "D:\SLIIT\Research\Repo\Organization\R24-066\Component 02\Augmentation\ml\Defect_Photos"

# S3 bucket name
s3_bucket_name = 'testminindu'

# Initialize S3 client
s3 = boto3.client('s3')

class S3SyncHandler(FileSystemEventHandler):
    def on_created(self, event):
        self.sync_to_s3(event.src_path) #passing the path of the created file or directory as an argument

    def on_modified(self, event):
        self.sync_to_s3(event.src_path) #passing the path of the modified file or directory as an argument

    def sync_to_s3(self, file_path):   #synchronize a local file to S3
        try:
            if os.path.isfile(file_path):  #checks if the file_path provided points to a valid file
                relative_path = os.path.relpath(file_path, local_folder)  #calculate relative path
                s3_key = os.path.join(os.path.basename(local_folder), relative_path)
                s3.upload_file(file_path, s3_bucket_name, s3_key) #constructs an S3 key
                logger.info(f"Uploaded {file_path} to S3 bucket {s3_bucket_name} as {s3_key}")
        except :
            logger.info(f" syncing {file_path} to S3")

if __name__ == "__main__":   #checks if the script is run as the main program
    # Initialize observer
    observer = Observer()
    observer.schedule(S3SyncHandler(), local_folder, recursive=True)

    try:
        logger.info(f"Watching local folder {local_folder} for changes...")
        observer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("Observer stopped by user.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
    finally:
        observer.join()