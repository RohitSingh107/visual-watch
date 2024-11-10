# TODO: Singleton class for data

import streamlit as st
import plotly.express as px
import streamlit as st
import pandas as pd
from utils.computes import compute
import plotly.express as px
import plotly.graph_objects as go
from icecream import ic

from utils.data import data_store

def display_table(title, data, columns):
    st.title(title)
    df = pd.DataFrame(data)
    st.dataframe(df[columns])


def plot_line_chart(data_series, chart_type):
    data = data_series.to_dict()

    # Convert keys to integers, find min and max years, and fill missing years with 0
    min_year, max_year = min(map(int, data)), max(map(int, data))
    full_data = {year: data.get(str(year), 0) for year in range(min_year, max_year + 1)}

    # Extract years and values for plotting
    years, values = zip(*sorted(full_data.items()))

    if chart_type == 'line':
        fig = go.Figure(go.Scatter(x=years, y=values, mode='lines+markers', name='Count'))
    else:
        fig = go.Figure(go.Bar(x=years, y=values, name='Count'))

    fig.update_layout(
        title="Data Over Years",
        xaxis_title="Year",
        yaxis_title="Count",
    )
    # Display the chart in Streamlit
    st.plotly_chart(fig)


# Title of the dashboard
st.title("Watch Dashboard")

# Sidebar for user inputs
st.sidebar.header("Input Parameters")

list_type = ["SEENLIST", "WATCHLIST"]


metrics = ["Rank Table", "Time Bar Chart", "Time Line Chart", "Countries Pie Chart", "Genre Pie Chart"]

selected_metrics = st.sidebar.multiselect("Select metrics to display", metrics, default=metrics)



if 'Rank Table' in selected_metrics:
    popular, imdb, tmdb, movies_data = data_store.get_lists()
    data = compute(popular, imdb, tmdb, movies_data)
    selected_columns = st.sidebar.multiselect("Select coumns to display", data[0].keys(), default=data[0].keys())
    display_table('Rank Table', data, selected_columns)


selected_list = st.sidebar.selectbox("Select List Type", list_type)
st.subheader(f"Showing data for {selected_list}")


year_counts = data_store.get_time_series(selected_list)
if 'Time Line Chart' in selected_metrics:
    # st.line_chart(year_counts)
    plot_line_chart(year_counts, chart_type = 'line')

if 'Time Bar Chart' in selected_metrics:
    plot_line_chart(year_counts, chart_type = 'bar')

if 'Countries Pie Chart' in selected_metrics:
    cpcn = st.sidebar.slider("Number of slices in Countries Pie Chart", value = 10, max_value=20, min_value=2) - 1

    country_count = data_store.get_countries_count(selected_list)

    country_count = {k: v for k, v in sorted(country_count.items(), key = lambda x: x[1], reverse=True)}

    values = list(country_count.values())
    names = list(country_count.keys())

    values = values[:cpcn] + [sum(values[cpcn:])]
    names = names[:cpcn] + ['Other']

    fig = px.pie(values= values, names= names, title='Countries Pie Chart')
    st.plotly_chart(fig)

if 'Genre Pie Chart' in selected_metrics:

    genre_count = data_store.get_genres_count(selected_list)

    genre_count = {k: v for k, v in sorted(genre_count.items(), key = lambda x: x[1], reverse=True)}

    values = list(genre_count.values())
    names = list(genre_count.keys())

    fig = px.pie(values= values, names= names, title='Genre Pie Chart')
    st.plotly_chart(fig)


