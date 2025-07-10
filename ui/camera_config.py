import streamlit as st

def camera_config_ui():
    st.sidebar.header("Dodaj Kamery")

    with st.sidebar.expander("❓ Jak znaleźć adres URL kamery?"):
        st.markdown("""
        - **MJPEG (strumień ruchomego obrazu, np. Bosch, Axis, Insecam)**:  
          `http://adres_ip:port/cgi-bin/faststream.jpg?...`  
          (strumień JPEG, wyświetlany jako video)

        - **Snapshot (pojedyncze zdjęcie, np. IP Webcam, proste kamery IP)**:  
          `http://adres_ip:port/shot.jpg` lub inne URL zwracające pojedynczy obraz JPEG  
          (w aplikacji obraz odświeżany co kilka sekund)

        - **RTSP (strumień wideo, np. Hikvision, Dahua)**:  
          `rtsp://user:pass@adres_ip:554/ścieżka`  
          (wymaga obsługi przez OpenCV, wymaga dostępu do kamery)

        - **HTTP/HTTPS strumienie JPEG (np. niektóre kamery IP)**:  
          `http://adres_ip:port/stream.mjpg` lub podobne  
          (działa podobnie jak MJPEG)

        🔐 **Uwaga:**  
        - Upewnij się, że kamera jest dostępna z miejsca, gdzie uruchamiasz aplikację (np. lokalna sieć lub publiczny adres).  
        - Niektóre kamery wymagają podania loginu i hasła w URL: `http://user:pass@adres_ip:port/...`  
        - Strumienie RTSP mogą nie działać na hostingu zdalnym (np. Streamlit Cloud) z powodu ograniczeń sieciowych.
        """)

    camera_url = st.sidebar.text_input("Dodaj kamerę URL")
    if st.sidebar.button("Dodaj kamerę") and camera_url:
        st.session_state.cameras.append(camera_url)
        st.sidebar.success(f"Kamera {camera_url} dodana!")
