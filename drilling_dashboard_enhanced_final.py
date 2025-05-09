
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Drilling Dashboard", layout="wide")
st.title("🛢️ Real-Time Drilling Dashboard")

@st.cache_data
def load_data():
    return pd.read_csv("your_cleaned_data_sample.csv")

df = load_data()

# --- Clean Timestamp values robustly ---
if "Timestamp" in df.columns:
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    df = df.dropna(subset=["Timestamp"])

    if not df.empty:
        st.sidebar.header("🔍 Filter Data")
        min_time = df["Timestamp"].min()
        max_time = df["Timestamp"].max()

        try:
            time_range = st.sidebar.slider("Select Time Range", min_value=min_time, max_value=max_time, value=(min_time, max_time))
            df = df[(df["Timestamp"] >= time_range[0]) & (df["Timestamp"] <= time_range[1])]
        except Exception as e:
            st.warning(f"Could not render time slider: {e}")
    else:
        st.warning("Timestamp column has no valid values.")
else:
    st.warning("Timestamp column missing from data.")

shaker_options = ["Total", "Shaker 1 load % (percent)", "Shaker 2 load % (NONE)", "Shaker 3 load % (NONE)"]
selected_shaker = st.sidebar.selectbox("Shaker Load Source", options=shaker_options)

# --- KPIs ---
if not df.empty:
    latest = df.iloc[-1]
    col1, col2, col3 = st.columns(3)
    col1.metric("Current ROP Efficiency", f"{latest['ROP Efficiency']:.4f}")
    col2.metric("Shaker Total Load", f"{latest['Shaker Total Load']:.2f} %")
    col3.metric("Total Alerts", int(df['ALERT'].sum()))

    # --- Plotly Chart for Shaker Load ---
    st.subheader("📊 Shaker Load Over Time")

    y_val = "Shaker Total Load" if selected_shaker == "Total" else selected_shaker

    fig1 = px.line(df, x="Timestamp", y=y_val, title=f"{y_val} Over Time")
    alert_df = df[df["ALERT"]]
    fig1.add_trace(go.Scatter(
        x=alert_df["Timestamp"],
        y=alert_df[y_val],
        mode='markers',
        marker=dict(color='red', size=6),
        name="Alerts"
    ))
    st.plotly_chart(fig1, use_container_width=True)

    # --- Plotly Chart for ROP Efficiency ---
    st.subheader("📈 ROP Efficiency Over Time")
    fig2 = px.line(df, x="Timestamp", y="ROP Efficiency", title="ROP Efficiency")
    fig2.add_hline(y=0.01, line_dash="dot", line_color="red", annotation_text="Alert Threshold")
    st.plotly_chart(fig2, use_container_width=True)

    # --- Optional Table ---
    with st.expander("📋 View Raw Data"):
        st.dataframe(df.tail(1000), use_container_width=True)
else:
    st.error("No valid data to display.")
