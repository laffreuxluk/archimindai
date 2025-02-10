import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app.pipeline import run_analysis
from config import INPUT_DIR
import logging

class CSVHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.csv'):
            logging.info(f"Nouveau fichier CSV détecté : {event.src_path}")
            run_analysis(event.src_path)

def start_watcher():
    if not os.path.exists(INPUT_DIR):
        os.makedirs(INPUT_DIR)
    event_handler = CSVHandler()
    observer = Observer()
    observer.schedule(event_handler, INPUT_DIR, recursive=False)
    observer.start()
    logging.info(f"Surveillance du dossier {INPUT_DIR} lancée.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
