import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# With a monthly view
# billing per unit,
# type of best-selling product, contribution per branch,
# Performance of payment methods…
# How are the branch reviews?

df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",")
df["Date"] = pd.to_datetime(df["Date"])
df=df.sort_values("Date")

df["Month Description"] = df["Date"].dt.strftime("%B, %Y")

month_descriptions = df["Month Description"].unique()
selected_description = st.sidebar.selectbox("Month, Year", month_descriptions)

# Filter by product category
product_categories = df["Product line"].unique()
selected_category = st.sidebar.multiselect("Product Category", product_categories)
df_filtered = df[df["Month Description"] == selected_description]
if selected_category:
    df_filtered = df_filtered[df_filtered["Product line"].isin(selected_category)]

col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

fig_date = px.bar(df_filtered, x="Date", y="Total", color="City", title="Revenue per day")
col1.plotly_chart(fig_date, use_container_width=True)

fig_prod = px.bar(df_filtered, x="Date", y="Product line", 
                  color="City", title="Revenue by product type",
                  orientation="h")
col2.plotly_chart(fig_prod, use_container_width=True)

city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()
fig_city = px.bar(city_total, x="City", y="Total",
                   title="Revenue by branch")
col3.plotly_chart(fig_city, use_container_width=True)

fig_kind = px.pie(df_filtered, values="Total", names="Payment",
                   title="Revenue by payment type")
col4.plotly_chart(fig_kind, use_container_width=True)

city_total = df_filtered.groupby("City")[["Rating"]].mean().reset_index()
fig_rating = px.bar(df_filtered, y="Rating", x="City",
                   title="Rating")
col5.plotly_chart(fig_rating, use_container_width=True)
