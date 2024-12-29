import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

# Log dosyasının yolu
LOG_FILE = "/home/bado/bsm/logs/changes.json"

class ChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        change_data = {
            "event_type": event.event_type,
            "src_path": event.src_path,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.log_change(change_data)

    @staticmethod
    def log_change(change):
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'w') as f:
                json.dump([], f)  # Boş bir JSON listesi başlat

        with open(LOG_FILE, 'r+') as f:
            data = json.load(f)
            data.append(change)
            f.seek(0)
            json.dump(data, f, indent=4)

if __name__ == "__main__":
    path = "/home/bado/bsm/test"  # İzlenecek dizin
    os.makedirs(path, exist_ok=True)

    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    print(f"İzleme başlatıldı: {path}")
    observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
