import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def create_average_by_weather_df(df):
  average_by_weather_df = df.groupby(by="weather").agg({
    "casual" : "mean",
    "registered" : "mean",
    "count" : "mean"
  }).reset_index()
  # average_by_weather_df.rename(columns={
  #   "count" :"count"
  # }, inplace=True)
  average_by_weather_df["weather"].replace({
    1: "Clear",
    2: "Mist",
    3: "Light Rain",
    4: "Heavy Rain"
  }, inplace=True)

  return average_by_weather_df

def create_average_by_weekdays_df(df):
  average_by_weekdays_df = df.groupby(by="weekday").agg({
    "casual" : "mean",
    "registered" : "mean",
    "count" : "mean"
  }).reset_index()
  # average_by_weekdays_df.rename(columns={
  #   "count" : "count"
  # }, inplace=True)
  average_by_weekdays_df["weekday"].replace({
    0: "Sunday",
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday"
  }, inplace=True)

  return average_by_weekdays_df

df = pd.read_csv("dashboard/main_data.csv")

df["date"] = pd.to_datetime(df["date"])

min_date = df["date"].min()
max_date = df["date"].max()

with st.sidebar:
  st.subheader("Filter")
  selected = st.selectbox(
    label="User Type",
    options=("Casual & Registered", "Casual", "Registered")
    
  )
  selected = "casual" if selected == "Casual" else ("registered" if selected == "Registered" else "count")
  start_date, end_date  = st.date_input(
    label="Interval Time", min_value=min_date, max_value=max_date,
    value=[min_date, max_date]
  )

main_df = df[(df["date"] >= str(start_date)) & (df["date"] <= str(end_date))]
average_by_weather_df = create_average_by_weather_df(main_df)
average_by_weekdays_df = create_average_by_weekdays_df(main_df)

st.header(":sparkles: Bike Sharing Analysis Dashboard :sparkles:")
st.subheader("Average Count of Rental Bikes by Weathers")
col1, col2 = st.columns(2)
with col1:
  average_max = average_by_weather_df[selected].max()
  day_max = average_by_weather_df[average_by_weather_df[selected] == average_max]
  st.metric("Highest Average", str(round(average_max)) + " (" + str(day_max["weather"].values[0]) + ")" )
with col2:
  average_min = average_by_weather_df[selected].min()
  day_min = average_by_weather_df[average_by_weather_df[selected] == average_min]
  st.metric("Lowest Average", str(round(average_min)) + " (" + str(day_min["weather"].values[0]) + ")" )

fig, ax = plt.subplots(figsize=(35,15))
sns.barplot(
  x=average_by_weather_df["weather"], 
  y=average_by_weather_df[selected],
  data=average_by_weather_df,
  ax=ax
)
ax.set_ylabel(None)
ax.set_xlabel(None)
# ax.set_title("Average Count of Rental Bikes Based on Weathers", loc="center", fontsize=50, y=1.1)
ax.tick_params(axis="x", labelsize=50)
ax.tick_params(axis="y", labelsize=50)
st.pyplot(fig)



st.subheader("")
st.subheader("")


st.subheader("Average Count of Rental Bikes by Weekdays")
col1, col2 = st.columns(2)
with col1:
  average_max = average_by_weekdays_df[selected].max()
  day_max = average_by_weekdays_df[average_by_weekdays_df[selected] == average_max]
  st.metric("Highest Average", str(round(average_max)) + " (" + str(day_max["weekday"].values[0]) + ")" )
with col2:
  average_min = average_by_weekdays_df[selected].min()
  day_min = average_by_weekdays_df[average_by_weekdays_df[selected] == average_min]
  st.metric("Lowest Average", str(round(average_min)) + " (" + str(day_min["weekday"].values[0]) + ")" )

  
fig, ax = plt.subplots(figsize=(35,15))
sns.barplot(
  x=average_by_weekdays_df["weekday"], 
  y=average_by_weekdays_df[selected],
  data=average_by_weekdays_df,
  ax=ax
)
ax.set_ylabel(None)
ax.set_xlabel(None)
# ax.set_title("Average Count of Rental Bikes Based on Weekdays", loc="center", fontsize=50, y=1.1)
ax.tick_params(axis="x", rotation=45, labelsize=50)
ax.tick_params(axis="y", labelsize=50)
st.pyplot(fig)
# st.markdown("##### Rental Bike Total : " + str(format(average_by_weekdays_df[("count", "sum")].sum(), ",")))
st.subheader("")
st.subheader("")
st.markdown("### Rental Bike Total : " + str(format(main_df[selected].sum(), ",")))
