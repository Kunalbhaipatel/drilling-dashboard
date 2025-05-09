
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🛢️ Drilling Shaker Monitoring Dashboard")

@st.cache_data
def load_data():
    return pd.read_csv("your_cleaned_data_sample.csv", parse_dates=["Timestamp"])

df = load_data()

st.metric("Total Alerts", int(df["ALERT"].sum()))
st.metric("Data Points", len(df))

st.subheader("Shaker Load Over Time")
fig, ax = plt.subplots()
ax.plot(df["Timestamp"], df["Shaker Total Load"], label="Total Load")
ax.scatter(df[df["ALERT"]]["Timestamp"], df[df["ALERT"]]["Shaker Total Load"], color='red', label="Alerts", s=10)
ax.set_xlabel("Time")
ax.set_ylabel("Shaker Load %")
ax.legend()
st.pyplot(fig)

st.subheader("ROP Efficiency Over Time")
fig2, ax2 = plt.subplots()
ax2.plot(df["Timestamp"], df["ROP Efficiency"], label="ROP Efficiency")
ax2.axhline(y=0.01, color="red", linestyle="--", label="Alert Threshold")
ax2.set_xlabel("Time")
ax2.set_ylabel("Efficiency")
ax2.legend()
st.pyplot(fig2)
