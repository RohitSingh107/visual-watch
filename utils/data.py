import pandas as pd

def get_lists():
    df = pd.read_csv('./sorting_spider.csv')
    hdf = pd.read_csv('./hindi_list.csv')
    hindi_list = map(lambda x: " ".join(x.split(' ')[:-1]), hdf['TITLE'].values)
    df['HINDI'] = df['TITLE'].isin(hindi_list) #type: ignore
    popular = df[df['SORTED BY'] == 'POPULAR'].drop(columns=['SORTED BY']).to_dict(orient='records') #type: ignore
    imdb = df[df['SORTED BY'] == 'IMDB_SCORE'].drop(columns=['SORTED BY']).to_dict(orient='records') #type: ignore
    tmdb = df[df['SORTED BY'] == 'TMDB_POPULARITY'].drop(columns=['SORTED BY']).to_dict(orient='records') #type: ignore

    return popular, imdb, tmdb
