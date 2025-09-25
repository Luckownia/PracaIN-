import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from fetchers.camera_fetcher import release_all_cameras
from session.state_manager import initialize_session_state
from fetchers.api_fetcher import fetch_data_from_api
from fetchers.database_fetcher import fetch_data_from_db
from fetchers.camera_fetcher import get_camera_frame
from charts.plotter import render_chart
import pymysql
pymysql.install_as_MySQLdb()


# Inicjalizacja sesji
initialize_session_state()

st.title("📊 Twój Dashboard")

#Odświeżanie aplikacji (by połączyć się z bazami danych w chmurach trzeba większy interval)
st_autorefresh(interval=1000, limit=None, key="data_refresh")

config_choice = st.sidebar.radio("Wybierz konfigurację", ["API", "Baza danych", "Kamery"])

# --- Obsługa API ---
if config_choice == "API":
    from ui.api_config import api_config_ui
    api_config_ui()

# --- Obsługa Bazy Danych ---
elif config_choice == "Baza danych":
    from ui.db_config import db_config_ui
    db_config_ui()

# --- Obsługa Kamer ---
elif config_choice == "Kamery":
    from ui.camera_config import camera_config_ui
    camera_config_ui()

st.subheader("📈 Dashboard")

# Łączenie wykresów i kamer w jeden grid
items = st.session_state.charts + st.session_state.cameras
num_cols = 3

for i in range(0, len(items), num_cols):
    cols = st.columns(num_cols)
    for j, item in enumerate(items[i:i + num_cols]):
        with cols[j]:
            # Wykres
            if isinstance(item, dict) and "title" in item:
                chart_id = item["id"]

                # Pobieranie nowych danych
                if item["source"] == "API":
                    new_data = fetch_data_from_api(item["api_url"], item["params"])
                else:
                    new_data = fetch_data_from_db(
                        item["db_connection"], item["query"],
                        st.session_state.db_type, item.get("collection_name", "")
                    )

                if not new_data.empty:
                    st.session_state.chart_data[chart_id] = pd.concat(
                        [st.session_state.chart_data[chart_id], new_data], ignore_index=True
                    )

                data = st.session_state.chart_data[chart_id]
                if "max_points" in item and len(data) > item["max_points"]:
                    data = data.tail(item["max_points"])

                fig = render_chart(item, data)
                st.plotly_chart(fig, use_container_width=True)

                # Usuwanie wykresu
                if st.button(f"🗑️ Usuń wykres {item['title']}", key=f"delete_chart_{chart_id}"):
                    del st.session_state.chart_data[chart_id]
                    st.session_state.charts = [c for c in st.session_state.charts if c["id"] != chart_id]
                    st.rerun()

            # Kamera
            else:
                camera = item
                st.markdown(f"**Kamera:** `{camera}`")

                if st.button(f"🗑️ Usuń kamerę {camera}", key=f"delete_camera_{camera}_{i}_{j}"):
                    st.session_state.cameras.remove(camera)
                    st.rerun()

                # Obsługa MJPEG lub snapshot
                if any(ext in camera.lower() for ext in [".jpg", ".jpeg", ".mjpg", "snapshot", "faststream"]):
                    st.image(camera, use_container_width=True)
                else:
                    frame = get_camera_frame(camera)
                    if frame is not None:
                        st.image(frame, channels="RGB", use_container_width=True)
                    else:
                        st.error(f"❌ Nie udało się pobrać obrazu z kamery: {camera}")

# Zwolnienie zasobów gdy brak kamer
if not st.session_state.cameras:
    release_all_cameras()
