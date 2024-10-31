import pandas as pd
import ast
from icecream import ic
from collections import defaultdict
import pycountry
from utils.misc import expand_genre 

def get_lists():
    df = pd.read_csv('./sorting_spider.csv')
    hdf = pd.read_csv('./hindi_list.csv')
    scrdf = pd.read_csv('./scrape_spider.csv')
    hindi_list = map(lambda x: " ".join(x.split(' ')[:-1]), hdf['TITLE'].values)
    df['HINDI'] = df['TITLE'].isin(hindi_list) #type: ignore
    df['YEAR'] = df['YEAR'].apply(lambda x: str(x))
    popular = df[df['SORTED BY'] == 'POPULAR'].drop(columns=['SORTED BY']).to_dict(orient='records') #type: ignore
    imdb = df[df['SORTED BY'] == 'IMDB_SCORE'].drop(columns=['SORTED BY']).to_dict(orient='records') #type: ignore
    tmdb = df[df['SORTED BY'] == 'TMDB_POPULARITY'].drop(columns=['SORTED BY']).to_dict(orient='records') #type: ignore

    movies_data = {f"{r['title']} ({r['year']})" : {"countries": r['countries'], "imdb_score" : r['imdb_score']} for r in scrdf.to_dict(orient='records')}

    return popular, imdb, tmdb, movies_data

def get_time_series(list_type):
    df = pd.read_csv('./scrape_spider.csv')
    df['year'] = df['year'].apply(lambda x: str(x))

    return df[df['list_type'] == list_type]['year'].value_counts()

def get_countries_count(list_type):
    df = pd.read_csv('./scrape_spider.csv')
    counts = defaultdict(int)
    for cl in df[df['list_type'] == list_type]['countries'].to_list():
        if type(cl) == float:
            continue
        for c in cl.split(','):
            counts[pycountry.countries.lookup(c).name] += 1

    return counts


def get_genres_count(list_type):
    df = pd.read_csv('./scrape_spider.csv')
    counts = defaultdict(int)
    for gl in df[df['list_type'] == list_type]['genres'].to_list():
        if type(gl) == float:
            continue
        for g in ast.literal_eval(gl):
            counts[expand_genre(g['shortName'])] += 1

    return counts
