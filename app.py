import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Weather Dashboard", layout="wide")

st.title("Weather Analysis Dashboard")
st.write("An interactive dashboard to explore historical weather data.")

@st.cache_data
def load_data():
    df = pd.read_csv("Climate of England _ Professional Reforms.csv")
    df['Formatted Date'] = pd.to_datetime(df['Formatted Date'])
    return df

df = load_data()

st.success("Weather data loaded successfully!")
st.write("Dataset Shape:", df.shape)

st.sidebar.header("Weather Filters")

months = sorted(df['Month'].dropna().unique())

selected_month = st.sidebar.selectbox(
    "Select Month",
    months
)

start_date = st.sidebar.date_input(
    "Start Date",
    df['Formatted Date'].min().date()
)

end_date = st.sidebar.date_input(
    "End Date",
    df['Formatted Date'].max().date()
)

filtered_df = df[
    (df['Month'] == selected_month) &
    (df['Formatted Date'].dt.date >= start_date) &
    (df['Formatted Date'].dt.date <= end_date)
]

st.subheader("Weather Statistics")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average Temperature",
    f"{filtered_df['Temperature (C)'].mean():.2f} °C"
)

col2.metric(
    "Highest Temperature",
    f"{filtered_df['Temperature (C)'].max():.2f} °C"
)

col3.metric(
    "Average Humidity",
    f"{filtered_df['Humidity'].mean():.2f}"
)

col4.metric(
    "Number of Days",
    filtered_df['Formatted Date'].dt.date.nunique()
)

st.subheader("1. Temperature Distribution")

fig, ax = plt.subplots(figsize=(8, 4))

ax.hist(filtered_df['Temperature (C)'], bins=30)

ax.set_title("Temperature Distribution")
ax.set_xlabel("Temperature (C)")
ax.set_ylabel("Frequency")

st.pyplot(fig)

st.subheader("2. Temperature vs Humidity")

fig, ax = plt.subplots(figsize=(8, 4))

ax.scatter(
    filtered_df['Temperature (C)'],
    filtered_df['Humidity'],
    alpha=0.3
)

ax.set_title("Temperature vs Humidity")
ax.set_xlabel("Temperature (C)")
ax.set_ylabel("Humidity")

st.pyplot(fig)

st.subheader("3. Average Temperature Over Time")

daily_temp = filtered_df.groupby(
    filtered_df['Formatted Date'].dt.date
)['Temperature (C)'].mean()

fig, ax = plt.subplots(figsize=(10, 4))

ax.plot(daily_temp.index, daily_temp.values)

ax.set_title("Average Temperature Over Time")
ax.set_xlabel("Date")
ax.set_ylabel("Average Temperature (C)")

plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)

st.subheader("4. Weather Correlation Heatmap")

corr = filtered_df[
    ['Temperature (C)', 'Humidity',
     'Wind Speed (km/h)',
     'Apparent Temperature (C)',
     'Visibility (km)',
     'Pressure (millibars)']
].corr()

fig, ax = plt.subplots(figsize=(8, 5))

sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)

ax.set_title("Weather Variables Correlation Heatmap")

st.pyplot(fig)

st.subheader("5. Average Wind Speed by Weather Condition")

avg_wind = filtered_df.groupby('Summary')['Wind Speed (km/h)'].mean().sort_values()

fig, ax = plt.subplots(figsize=(10, 5))

avg_wind.plot(kind='bar', ax=ax)

ax.set_title("Average Wind Speed by Weather Condition")
ax.set_xlabel("Weather Condition")
ax.set_ylabel("Average Wind Speed (km/h)")

plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)

st.subheader("Raw Weather Data")
show_data = st.checkbox("Show Raw Data Table")

if show_data:
    st.dataframe(filtered_df)



