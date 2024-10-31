import pandas as pd

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
