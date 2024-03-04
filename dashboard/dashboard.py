import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def create_average_by_weather_df(df):
  average_by_weather_df = df.groupby(by="weather").agg({
    "count" : "mean"
  }).sort_values(by="count", ascending=False).reset_index()
  average_by_weather_df.rename(columns={
    "count" :"average"
  }, inplace=True)
  average_by_weather_df["weather"].replace({
    1: "Clear",
    2: "Mist",
    3: "Light Rain",
    4: "Heavy Rain"
  }, inplace=True)

  return average_by_weather_df

def create_average_by_weekdays_df(df):
  average_by_weekdays_df = df.groupby(by="weekday").agg({
    "count" : "mean"
  }).reset_index()
  average_by_weekdays_df.rename(columns={
    "count" : "average"
  }, inplace=True)
  average_by_weekdays_df["weekday"] = average_by_weekdays_df["weekday"].replace({
    0: "Sunday",
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday"
  })

  return average_by_weekdays_df

df = pd.read_csv("dashboard\main_data.csv")
average_by_weather_df = create_average_by_weather_df(df)
average_by_weekdays_df = create_average_by_weekdays_df(df)

st.header(":sparkles: Bike Sharing Analysis Dashboard :sparkles:")

col1, col2 = st.columns(2)


# st.subheader("Average Count of Rental Bikes Based on Weekdays")
fig, ax = plt.subplots(figsize=(35,15))
sns.barplot(
  x=average_by_weekdays_df["weekday"], 
  y=average_by_weekdays_df["average"],
  data=average_by_weekdays_df,
  ax=ax
)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.set_title("Average Count of Rental Bikes Based on Weekdays", loc="center", fontsize=60, y=1.12)
ax.tick_params(axis="x", rotation=45, labelsize=50)
ax.tick_params(axis="y", labelsize=50)
st.pyplot(fig)


st.subheader("")
st.subheader("")
fig, ax = plt.subplots(figsize=(35,15))
sns.barplot(
  x=average_by_weather_df["weather"], 
  y=average_by_weather_df["average"],
  data=average_by_weather_df,
  ax=ax
)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.set_title("Average Count of Rental Bikes Based on Weathers", loc="center", fontsize=60, y=1.12)
ax.tick_params(axis="x", labelsize=50)
ax.tick_params(axis="y", labelsize=50)
st.pyplot(fig)

