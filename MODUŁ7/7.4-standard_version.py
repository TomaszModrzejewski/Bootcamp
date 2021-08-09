import random
from faker import Faker
fake = Faker()


class Movie:
    def __init__(self, title, year, genre):
        self.title = title
        self.year = year
        self.genre = genre
        self.current_reps = 0

    def play(self, step=1):
        self.current_reps += step

    def __str__(self):
        return f'{self.title} ({self.year})'

    def __repr__(self):
        return f'{self.title} ({self.year})'


class Series(Movie):
    def __init__(self, episode, season, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.episode = episode
        self.season = season

    def __str__(self):
        return f'{self.title} S{self.season}E{self.episode}'

    def __repr__(self):
        return f'{self.title} S{self.season}E{self.episode}'


def search(title):
    if self.title == title:
        print('Działa!')


def create_Movie(type, amount):
    for i in range(0, amount):
        Movies = Movie(fake.first_name(), fake.year(), fake.last_name())
        print(Movies)

Movie1 = Movie('Pulp Fiction', '1994', 'Comedy')
Movie2 = Movie('Pszczółka maja', '1989', 'Animation')

Series1 = Series('01', '01', 'How i meet your mother', '2000', 'Comedy')
Series2 = Series('02', '05', 'Narcos', '2019', 'Action')

print(Movie1)
print(Movie1.current_reps)

print(Series1)
print(Series1.current_reps)

List = (Movie1, Movie2, Series1, Series2)


def generate_views():
    times = random.randint(0, 100)
    choice = random.choice(List)
    print(choice)
    choice.play(times)
