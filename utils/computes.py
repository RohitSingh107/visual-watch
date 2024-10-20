
from collections import defaultdict
def average_rank(popular, imdb, tmdb):
    if not (len(popular) == len(imdb) == len(tmdb)):
        raise ValueError("Lengths of input lists are not equal")

    # Create a dictionary to hold the rank sums
    rank_sums = defaultdict(float)
    
    # Function to get a unique key for each movie
    def get_key(movie):
        return f"{movie['TITLE']} ({movie['YEAR']})"

    # Assign ranks based on the list position
    for lst in [popular, imdb, tmdb]:
        for i, movie in enumerate(lst):
            rank_sums[get_key(movie)] += i + 1  # Rank is index + 1

    # Calculate the average rank for each element
    rank_averages = {key: rank_sum / 3 for key, rank_sum in rank_sums.items()}

    # Create a new list with average ranks included
    overall_ranked_average = []
    for movie in imdb:
        key = get_key(movie)
        new_movie = movie.copy()  # Create a copy to avoid modifying the original
        new_movie['AVERAGE_RANK'] = rank_averages[key]
        overall_ranked_average.append(new_movie)

    # Sort the elements by average rank
    overall_ranked_average.sort(key=lambda x: x['AVERAGE_RANK'])

    return overall_ranked_average
