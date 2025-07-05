import streamlit as st

def camera_config_ui():
    st.sidebar.header("Dodaj Kamery")

    with st.sidebar.expander("❓ Jak znaleźć adres URL kamery?"):
        st.markdown("""
        - **Kamery IP (np. Hikvision, Dahua)**:  
          `rtsp://użytkownik:hasło@adres_ip:554/ścieżka`
        - **Aplikacja IP Webcam (Android)**:  
          `http://adres_ip:port/video`
        - **Kamery MJPEG lub HTTP streaming**:  
          `http://adres_ip:port/stream.mjpg` lub podobny  

        🔐 **Wskazówka**: Adres znajdziesz w instrukcji kamery, aplikacji mobilnej lub panelu konfiguracyjnym routera (zakładka „urządzenia w sieci”).
        """)

    camera_url = st.sidebar.text_input("Dodaj kamerę URL")
    if st.sidebar.button("Dodaj kamerę") and camera_url:
        st.session_state.cameras.append(camera_url)
        st.sidebar.success(f"Kamera {camera_url} dodana!")
