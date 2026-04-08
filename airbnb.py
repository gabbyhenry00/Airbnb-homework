import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Gabriella Henry")

df = pd.read_csv("airbnb_data.csv")
df = df.dropna(subset=["room_type", "neighbourhood_group", "price"])

with st.sidebar:
    st.title("Search Filters")
    available_neighborhoods = df["neighbourhood_group"].unique()
    neigh = st.multiselect(
        "What District do you want to select?",
        available_neighborhoods,
        default=available_neighborhoods
    )
    available_room_types = df["room_type"].unique()
    room_type = st.multiselect(
        "What Room Type do you want to select?",
        available_room_types,
        default=available_room_types
    )
    price_max = st.slider("Select max price", float(df["price"].min()), 500.0)

df_filtered = df[
    df["neighbourhood_group"].isin(neigh) &
    df["room_type"].isin(room_type) &
    (df["price"] < price_max)
]

col1, col2, col3 = st.columns(3)
col1.metric("Number of listings", len(df_filtered))
with col2:
    if len(df_filtered) > 0:
        avg_price = df_filtered["price"].mean()
        st.metric("Average Price", f"${avg_price:.2f}")
    else:
        st.metric("Average Price", "$0.00")
with col3:
    if len(df_filtered) > 0:
        avg_nights = df_filtered["minimum_nights"].mean()
        st.metric("Avg Min Nights", f"{avg_nights:.1f}")
    else:
        st.metric("Avg Min Nights", "0")

tab1, tab2 = st.tabs(["Listing Analysis", "Neighbourhood Analysis"])

with tab1:
    st.subheader("Number of Listings by Room Type")
    room_counts = df_filtered.groupby("room_type").size().reset_index(name="count")
    fig1 = px.bar(
        room_counts,
        x="room_type",
        y="count",
        color="room_type",
        title="Number of Listings by Room Type"
    )
    st.plotly_chart(fig1)

    st.subheader("Average Price by Room Type")
    avg_price_type = df_filtered.groupby("room_type")["price"].mean().reset_index()
    fig2 = px.bar(
        avg_price_type,
        x="room_type",
        y="price",
        color="room_type",
        title="Average Price by Room Type"
    )
    st.plotly_chart(fig2)

with tab2:
    st.subheader("Top 15 Neighbourhoods by Reviews per Month")
    top_neigh = df_filtered.groupby("neighbourhood")["reviews_per_month"].mean().nlargest(15).reset_index()
    fig3 = px.bar(
        top_neigh,
        x="reviews_per_month",
        y="neighbourhood",
        orientation="h",
        color="reviews_per_month",
        title="Average Reviews per Month by Neighbourhood"
    )
    st.plotly_chart(fig3)

    st.subheader("Number of Reviews vs Price")
    fig4 = px.scatter(
        df_filtered,
        x="number_of_reviews",
        y="price",
        color="room_type",
        title="Number of Reviews vs Price"
    )
    st.plotly_chart(fig4)

    st.subheader("Map of Listings in Madrid")
    st.map(df_filtered[["latitude", "longitude"]].dropna())

with st.expander("See filtered data"):
    st.dataframe(df_filtered)