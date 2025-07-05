import cv2

# Przechowywanie aktywnych połączeń kamer
camera_streams = {}
camera_fail_count = {}

def get_camera_frame(url):
    try:
        # Jeśli kamera jeszcze nie została zainicjowana lub nie działa
        if url not in camera_streams or not camera_streams[url].isOpened():
            camera_streams[url] = cv2.VideoCapture(url)
            camera_fail_count[url] = 0

        cap = camera_streams[url]
        success, frame = cap.read()

        if success and frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            camera_fail_count[url] = 0  # zresetuj licznik błędów
            return frame
        else:
            # Zwiększ licznik błędów
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
    # Kopiuj klucze do osobnej listy, by nie zmieniać słownika w czasie iteracji
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
