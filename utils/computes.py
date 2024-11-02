import pycountry
from collections import defaultdict, deque
from typing import Dict

# Function to get a unique key for each movie
def get_key(movie):
    return f"{movie['TITLE']} ({movie['YEAR']})"

def compute(popular, imdb, tmdb, movies_data):
    if not (len(popular) == len(imdb) == len(tmdb)):
        raise ValueError("Lengths of input lists are not equal")

    r = add_average_rank(imdb, popular, imdb, tmdb)
    r = add_combined_points_imdb_weighted(r, popular, imdb, tmdb, movies_data)

    r = add_countries(r, movies_data)

    r.sort(key=lambda x: x['AVERAGE_RANK'])
    return r


def add_average_rank(movies, popular, imdb, tmdb):

    # Create a dictionary to hold the rank sums
    rank_sums = defaultdict(float)

    # Assign ranks based on the list position
    for lst in [popular, imdb, tmdb]:
        for i, movie in enumerate(lst):
            rank_sums[get_key(movie)] += i + 1  # Rank is index + 1

    rank_averages = {key: round(rank_sum / 3, 2) for key, rank_sum in rank_sums.items()}

    # Create a new list with average ranks included
    overall_ranked_average = deque()
    for movie in movies:
        key = get_key(movie)
        new_movie = movie.copy()  # Create a copy to avoid modifying the original
        new_movie['AVERAGE_RANK'] = rank_averages[key]
        overall_ranked_average.append(new_movie)

    return list(overall_ranked_average)


def add_combined_points_imdb_weighted(movies, popular, imdb, tmdb, movies_data):

    points = defaultdict(int)

    for lst in [popular, imdb, tmdb]:
        for i, movie in enumerate(reversed(lst)):
            points[get_key(movie)] += i + 1

    weighted_points = {key : round(point * movies_data[key]['imdb_score']) for key, point in points.items()}
    overall_weighted_points = deque()
    for movie in movies:
        key = get_key(movie)
        new_movie = movie.copy()
        new_movie['IMDB_WEIGHTED'] = weighted_points[key]
        overall_weighted_points.append(new_movie)

    return list(overall_weighted_points)

def add_countries(movies, movies_data):
    new_list = deque()

    for movie in movies:
        key = get_key(movie)

        c = movies_data[key]['countries']
        if type(c) == float:
            countries = []
        else:
            countries = c.split(',')

        new_movie = movie.copy()
        new_movie['INTERNATIONAL'] = not 'US' in countries and not 'IN' in countries 
        new_movie['COUNTRIES'] = list(map(lambda x : pycountry.countries.lookup(x).name, countries))
        new_list.append(new_movie)

    return list(new_list)



