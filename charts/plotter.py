import plotly.graph_objs as go
import streamlit as st
import uuid

def render_chart(chart_config, data):
    chart_type = chart_config["type"]
    x = data[chart_config["x_column"]]
    y = data[chart_config["y_column"]]

    fig = go.Figure()
    if chart_type == "Liniowy":
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers"))
    elif chart_type == "Słupkowy":
        fig.add_trace(go.Bar(x=x, y=y))
    elif chart_type == "Punktowy":
        fig.add_trace(go.Scatter(x=x, y=y, mode="markers"))

    st.plotly_chart(fig, use_container_width=True, key=str(uuid.uuid4()))
