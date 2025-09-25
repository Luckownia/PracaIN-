import plotly.graph_objs as go
import pandas as pd

def render_chart(chart_config, data: pd.DataFrame) -> go.Figure:
    """
    Tworzy wykres Plotly na podstawie konfiguracji i danych.

    Args:
        chart_config (dict): Konfiguracja wykresu (type, x_column, y_column, title).
        data (pd.DataFrame): Dane do wykresu.

    Returns:
        go.Figure: Obiekt wykresu Plotly.
    """
    chart_type = chart_config.get("type", "Liniowy")
    x_col = chart_config.get("x_column")
    y_col = chart_config.get("y_column")

    # Sprawdzenie, czy kolumny istnieją w danych
    if x_col not in data.columns or y_col not in data.columns:
        fig = go.Figure()
        fig.update_layout(title="Brak danych do wyświetlenia")
        return fig

    x = data[x_col]
    y = data[y_col]

    fig = go.Figure()

    if chart_type == "Liniowy":
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers", name=chart_config.get("title", "")))
    elif chart_type == "Słupkowy":
        fig.add_trace(go.Bar(x=x, y=y, name=chart_config.get("title", "")))
    elif chart_type == "Punktowy":
        fig.add_trace(go.Scatter(x=x, y=y, mode="markers", name=chart_config.get("title", "")))
    else:
        # Domyślnie liniowy
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers", name=chart_config.get("title", "")))

    # Ustawienia layoutu
    fig.update_layout(
        title=chart_config.get("title", ""),
        xaxis_title=x_col,
        yaxis_title=y_col,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig
