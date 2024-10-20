import streamlit as st
import pandas as pd
from utils.computes import average_rank
from icecream import ic

from utils.data import get_lists

# Title of the dashboard
st.title("Watch Dashboard")

# Sidebar for user inputs
st.sidebar.header("Input Parameters")

list_type = ["Watchlist", "Seenlist"]

selected_list = st.sidebar.selectbox("Select List Type", list_type)

metrics = ["Average Rank", "Average Rank International"]

selected_metrics = st.sidebar.multiselect("Select metrics to display", metrics, default=metrics)

st.subheader(f"Showing data for {selected_list}")

def display_table(title, data):
    st.title(title)
    df = pd.DataFrame(data)
    st.dataframe(df)

if 'Average Rank' in selected_metrics:
    popular, imdb, tmdb = get_lists()
    data = average_rank(popular, imdb, tmdb)
    display_table('Average Rank', data)


# if 'Average Rank International' in metrics:
#     show_table(st, 'Average Rank International', [1,2,3])
