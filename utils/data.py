import pandas as pd
import ast
from icecream import ic
from collections import defaultdict
import pycountry
from utils.misc import expand_genre 


class DataStore:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DataStore, cls).__new__(cls, *args, **kwargs)
            cls._instance._lists = None 
            cls._instance._sorting_df = None 
            cls._instance._scrape_df = None 
            cls._instance._hindi_df = None 
            cls._instance._hot_df = None 
            cls._instance._time_series = {} 
            cls._instance._genres_count = {} 
            cls._instance._countries_count = {} 
        return cls._instance

    def _generate_hindi_df(self):
        return pd.read_csv('./hindi_list.csv')
    def _generate_hot_df(self):
        return pd.read_csv('./hot_list.csv')
    def _generate_scrape_df(self):
        return pd.read_csv('./scrape_spider.csv')
    def _generate_sorting_df(self):
        return pd.read_csv('./sorting_spider.csv')

    def _get_hot_df(self):
        if self._hot_df is None:
            self._hot_df = self._generate_hot_df()
        return self._hot_df

    def _get_hindi_df(self):
        if self._hindi_df is None:
            self._hindi_df = self._generate_hindi_df()
        return self._hindi_df

    def _get_scrape_df(self):
        if self._scrape_df is None:
            self._scrape_df = self._generate_scrape_df()
        return self._scrape_df

    def _get_sorting_df(self):
        if self._sorting_df is None:
            self._sorting_df = self._generate_sorting_df()
        return self._sorting_df

    def _generate_lists(self):
        df = self._get_sorting_df() 
        hdf = self._get_hindi_df() 
        hldf = self._get_hot_df() 
        scrdf = self._get_scrape_df() 
        hindi_list = map(lambda x: " ".join(x.split(' ')[:-1]), hdf['TITLE'].values)
        hot_list = map(lambda x: " ".join(x.split(' ')[:-1]), hldf['TITLE'].values)
        df['HINDI'] = df['TITLE'].isin(hindi_list) #type: ignore
        df['HOT'] = df['TITLE'].isin(hot_list) #type: ignore
        df['YEAR'] = df['YEAR'].apply(lambda x: str(x))
        df['IS MOVIE'] = df['ID'].str.startswith('tm')
        popular = df[df['SORTED BY'] == 'POPULAR'].drop(columns=['SORTED BY']).to_dict(orient='records') #type: ignore
        imdb = df[df['SORTED BY'] == 'IMDB_SCORE'].drop(columns=['SORTED BY']).to_dict(orient='records') #type: ignore
        tmdb = df[df['SORTED BY'] == 'TMDB_POPULARITY'].drop(columns=['SORTED BY']).to_dict(orient='records') #type: ignore

        movies_data = {f"{r['title']} ({r['year']})" : {"countries": r['countries'], "imdb_score" : r['imdb_score']} for r in scrdf.to_dict(orient='records')}

        return popular, imdb, tmdb, movies_data


    def _generate_time_series(self, list_type):
        df = self._get_scrape_df() 
        df['year'] = df['year'].apply(lambda x: str(x))

        return df[df['list_type'] == list_type]['year'].value_counts()

    def _generate_countries_count(self, list_type):
        df = self._get_scrape_df() 
        counts = defaultdict(int)
        for cl in df[df['list_type'] == list_type]['countries'].to_list():
            if type(cl) == float:
                continue
            for c in cl.split(','):
                counts[pycountry.countries.lookup(c).name] += 1

        return counts


    def _generate_genres_count(self, list_type):
        df = self._get_scrape_df() 
        counts = defaultdict(int)
        for gl in df[df['list_type'] == list_type]['genres'].to_list():
            if type(gl) == float:
                continue
            for g in ast.literal_eval(gl):
                counts[expand_genre(g['shortName'])] += 1

        return counts

    def get_time_series(self, list_type):
        if list_type not in  self._time_series:
            self._time_series[list_type] = self._generate_time_series(list_type)
        return self._time_series[list_type]

    def get_genres_count(self, list_type):
        if list_type not in  self._genres_count:
            self._genres_count[list_type] = self._generate_genres_count(list_type)
        return self._genres_count[list_type]

    def get_countries_count(self, list_type):
        if list_type not in  self._countries_count:
            self._countries_count[list_type] = self._generate_countries_count(list_type)
        return self._countries_count[list_type]

    def get_lists(self):
        if self._lists is None:
            self._lists = self._generate_lists()
        return self._lists


    def reset_data(self):
        self._lists = None
        self._sorting_df = None 
        self._scrape_df = None 
        self._hindi_df = None 
        self._hot_df = None 
        self._time_series = {} 
        self._genres_count = {} 
        self._countries_count = {} 

data_store = DataStore()

