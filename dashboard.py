import streamlit as st
import pandas as pd
from utils.computes import compute
from icecream import ic

from utils.data import get_lists

# Title of the dashboard
st.title("Watch Dashboard")

# Sidebar for user inputs
st.sidebar.header("Input Parameters")

list_type = ["Watchlist", "Seenlist"]

selected_list = st.sidebar.selectbox("Select List Type", list_type)

metrics = ["Rank Table", "Test"]

selected_metrics = st.sidebar.multiselect("Select metrics to display", metrics, default=metrics)

st.subheader(f"Showing data for {selected_list}")

def display_table(title, data, columns):
    st.title(title)
    df = pd.DataFrame(data)
    st.dataframe(df[columns])

if 'Rank Table' in selected_metrics:
    popular, imdb, tmdb, movies_data = get_lists()
    data = compute(popular, imdb, tmdb, movies_data)
    selected_columns = st.sidebar.multiselect("Select coumns to display", data[0].keys(), default=data[0].keys())
    display_table('Rank Table', data, selected_columns)


# if 'Average Rank International' in metrics:
#     show_table(st, 'Average Rank International', [1,2,3])
