import time
import os
import requests
import webbrowser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_FOLDER = "/Users/mark/Social_Posts"
UPLOAD_URL = "https://caption-backend-clean-1.onrender.com/upload-preview"

VALID_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")

processed_files = set()


def wait_until_file_is_ready(file_path, checks=3, delay=0.75):
    """Wait until Lightroom has finished writing the exported image."""
    last_size = -1
    stable_count = 0

    while stable_count < checks:
        try:
            current_size = os.path.getsize(file_path)
        except OSError:
            time.sleep(delay)
            continue

        if current_size == last_size and current_size > 0:
            stable_count += 1
        else:
            stable_count = 0

        last_size = current_size
        time.sleep(delay)

class NewImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path

        if not file_path.lower().endswith(VALID_EXTENSIONS):
            return

        if file_path in processed_files:
            return

        processed_files.add(file_path)

        print(f"New image found: {file_path}")

        # Wait for Lightroom to finish writing the exported file
        wait_until_file_is_ready(file_path)

        try:
            with open(file_path, "rb") as image_file:
                response = requests.post(
                    UPLOAD_URL,
                    files={"image": image_file},
                    timeout=60
                )

            response.raise_for_status()
            data = response.json()

            page_url = data.get("page_url")

            if page_url:
                print(f"Opening: {page_url}")
                webbrowser.open(page_url)

                # Open Adobe Express as well
                time.sleep(1)
                webbrowser.open("https://express.adobe.com")
            else:
                print("No page_url returned:", data)

        except Exception as e:
            print("Upload failed:", e)


if __name__ == "__main__":
    os.makedirs(WATCH_FOLDER, exist_ok=True)

    observer = Observer()
    observer.schedule(NewImageHandler(), WATCH_FOLDER, recursive=False)
    observer.start()

    print(f"Watching folder: {WATCH_FOLDER}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
