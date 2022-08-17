import csv
from collections import Counter, defaultdict, OrderedDict, namedtuple

MOVIE_DATA = 'movie_metadata.csv'
MIN_YEAR = 1960
MIN_MOVIES = 4
NUM_TOP_DIRECTORS = 20
LINE_CHAR_LIMIT = 80

def print_director_line(num, director, rating):
    num = str(num).strip()
    director = director.strip()
    rating = str(round(rating, 1))
    spaces = LINE_CHAR_LIMIT - len(str(num)) - len(director) - len(str(rating)) - 2
    print(f"{num}. {director}{' ' * spaces}{rating}")

def print_movie_line(year, title, rating):
    year = str(year).strip()
    title = title.strip()
    rating = str(round(float(rating), 1))
    spaces = LINE_CHAR_LIMIT - len(str(year)) - len(title) - len(str(rating)) - 2
    print(f"{year}] {title}{' ' * spaces}{rating}")


Movie = namedtuple('Movie', 'director title year score')

# These are the headings/columns that are valuable to us
headings = ['director_name', 'movie_title', 'title_year', 'imdb_score']

# get all of the movie data
with open(MOVIE_DATA) as csvfile:
    reader = csv.DictReader(csvfile)
    data = [
        {
            k: v
            for k, v in row.items()
            if k in headings
        }
        for row in reader
    ]

# We only want to consider movies after 1960
data = [item for item in data if int('0'+item['title_year']) >= MIN_YEAR]

# We only want directors with 4 or more movies
directors = {
    director: count
    for director, count in Counter([item['director_name'] for item in data]).items()
    if count >= MIN_MOVIES
}
data = [item for item in data if item['director_name'] in directors.keys()]

# get 20 highest rated directors
directors_ratings = defaultdict(float)
for item in data:
    directors_ratings[item['director_name']] += (float(item['imdb_score'])/directors[item['director_name']])
directors_ratings = OrderedDict(sorted(directors_ratings.items(), key=lambda x: x[1], reverse=True)[:NUM_TOP_DIRECTORS])
print(directors_ratings)

for i, (director, rating) in enumerate(directors_ratings.items()):
    print_director_line(i+1, director, rating)
    print(f"{'-' * 80}")
    movies = sorted([movie for movie in data if director in movie['director_name']], key=lambda x: float(x['imdb_score']), reverse=True)
    for movie in movies:
        print_movie_line(movie['title_year'], movie['movie_title'], movie['imdb_score'])
    print("\n")
