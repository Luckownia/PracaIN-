import cv2
import requests
from PIL import Image
from io import BytesIO

# Przechowywanie aktywnych połączeń kamer
camera_streams = {}
camera_fail_count = {}

def is_jpeg_snapshot_url(url):
    #Wykrywanie czy to snapshot JPEG
    return any(x in url.lower() for x in ["shot.jpg", "faststream.jpg", ".jpg?"])

def get_jpeg_snapshot_frame(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            return image.convert("RGB")
        else:
            print(f"❌ Błąd HTTP {response.status_code} dla {url}")
            return None
    except Exception as e:
        print(f"❌ Błąd przy pobieraniu JPEG z {url}: {e}")
        return None

def get_camera_frame(url):
    # Obsługa snapshotów JPEG
    if is_jpeg_snapshot_url(url):
        return get_jpeg_snapshot_frame(url)

    # Obsługa klasycznych strumieni RTSP / MJPEG
    try:
        if url not in camera_streams or not camera_streams[url].isOpened():
            camera_streams[url] = cv2.VideoCapture(url)
            camera_fail_count[url] = 0

        cap = camera_streams[url]
        success, frame = cap.read()

        if success and frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            camera_fail_count[url] = 0
            return frame
        else:
            camera_fail_count[url] += 1
            if camera_fail_count[url] > 5:
                print(f"❌ Kamera {url} nie odpowiada — zamykam połączenie.")
                cap.release()
                del camera_streams[url]
                del camera_fail_count[url]
            return None

    except Exception as e:
        print(f"❌ Błąd przy pobieraniu ramki z kamery {url}: {e}")
        return None

def release_all_cameras():
    for url in list(camera_streams.keys()):
        try:
            cap = camera_streams[url]
            if cap.isOpened():
                cap.release()
        except Exception as e:
            print(f"Błąd przy zwalnianiu kamery {url}: {e}")
        finally:
            camera_streams.pop(url, None)
            camera_fail_count.pop(url, None)
