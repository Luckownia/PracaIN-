# 📊 Generator Live Dashboard

**Generator Live Dashboard** to wszechstronny dashboard stworzony w Streamlit, który umożliwia wizualizację danych z różnych źródeł — API, baz danych (PostgreSQL, MySQL, MongoDB) oraz strumieni z kamer na żywo.

---

## 🚀 Funkcje

- 🔌 **Połączenia API** – pobieraj dane z zewnętrznych API i twórz wykresy w czasie rzeczywistym.
- 🛢️ **Obsługa baz danych** – wizualizuj dane z PostgreSQL, MySQL i MongoDB.
- 🎥 **Podgląd z kamer** – dodaj strumienie RTSP/HTTP i oglądaj obraz na żywo.
- 📈 **Dynamiczne wykresy** – generowanie wykresów liniowych, słupkowych i punktowych z Plotly.

---

## 🧰 Technologie

- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/python/)
- [OpenCV](https://opencv.org/) – obsługa kamer
- [SQLAlchemy](https://www.sqlalchemy.org/) – obsługa relacyjnych baz danych
- [PyMongo](https://pymongo.readthedocs.io/en/stable/) – obsługa MongoDB

---

## 🖥️ Filmy




https://github.com/user-attachments/assets/3f9e6dac-3607-438e-b860-1f5297db30c6



https://github.com/user-attachments/assets/3d1967cd-cd53-4711-9ff1-82a1f3652997




https://github.com/user-attachments/assets/63286594-3f89-4ad6-abc2-adb010eddae0




https://github.com/user-attachments/assets/c8e63a98-1253-4edf-93be-882f3641fec3




---

## 🔧 Uruchamianie projektu

### 1. Klonowanie repozytorium

```bash
git clone https://github.com/Luckownia/PracaIN-.git
```

### 2. Pobranie wymaganych biblotek
```bash
pip install -r requirements.txt
```
### 3. Uruchomienie Aplikacji 

```bash
streamlit run .\main.py
```

---

## 🧪 Tryby działania aplikacji

Po uruchomieniu aplikacji w przeglądarce (domyślnie `http://localhost:8501`) w panelu bocznym możesz wybrać jeden z trybów:

### 🔹 API
- Wprowadź adres URL API oraz opcjonalne parametry zapytania w formacie JSON.
- Kliknij „Pobierz dane z API”, a następnie skonfiguruj wykres: tytuł, typ, kolumny X/Y oraz liczbę punktów.
- Obsługiwane typy wykresów: Liniowy, Słupkowy, Punktowy.

### 🔹 Baza danych
- Wybierz typ bazy: PostgreSQL, MySQL lub MongoDB.
- Wprowadź dane połączenia, zapytanie SQL lub kolekcję (dla MongoDB).
- Po załadowaniu danych wybierz kolumny do wykresu oraz jego typ.

### 🔹 Kamery
- Dodaj adres URL strumienia z kamery (np. RTSP, MJPEG, HTTP).
- Aplikacja pokaże obraz na żywo w czasie rzeczywistym.
- Możesz dodawać i usuwać wiele kamer dynamicznie.

---

## 🗂️ Struktura katalogów

├── main.py # Główna aplikacja Streamlit

├── charts/

│ └── plotter.py # Tworzenie wykresów (Plotly)

├── fetchers/

│ ├── api_fetcher.py # Pobieranie danych z API

│ ├── camera_fetcher.py # Obsługa kamer (OpenCV)

│ └── database_fetcher.py # Obsługa baz danych SQL/MongoDB/PostreSql

├── session/

│ └── state_manager.py # Utrzymywanie stanu sesji użytkownika

├── ui/

│ ├── api_config.py # UI do konfiguracji API i wykresów

│ ├── camera_config.py # UI do dodawania i zarządzania kamerami

│ └── db_config.py # UI do konfiguracji połączenia z bazą danych

└── requirements.txt # Lista biblotek
