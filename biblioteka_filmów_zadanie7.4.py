import faker
import random
from datetime import date

today = date.today()
d1 = today.strftime("%d.%m.%Y")

fake = faker.Faker()


class Movie:

    def __init__(self, title: str, release_year: str, genre: str, watch_amount: int):
        self.title = title
        self.release_year = release_year
        self.genre = genre
        self.watch_amount = watch_amount

    def __str__(self):
        return f"{self.title} {self.release_year}"

    def play(self):
        self.watch_amount += 1


class Series(Movie):

    def __init__(self,
                 title: str,
                 release_year: str,
                 genre: str,
                 watch_amount: int,
                 season_number: str,
                 episode_number: str
                 ):
        super().__init__(title, release_year, genre, watch_amount)
        self.season_number = season_number
        self.episode_number = episode_number

    def __str__(self):
        return f"{self.title} {self.season_number}{self.episode_number}"

    def play(self):
        self.watch_amount += 1


class Library:

    def __init__(self, name: str, movies_list=None):
        self.name = name
        self._movies_list = movies_list or []

    def print_all_movies(self):
        print("\n".join([str(entry) for entry in self._movies_list]))

    def get_all(self):
        return self._movies_list.copy()

    def get_movies(self):
        return [entry for entry in self._movies_list if not isinstance(entry, Series)]

    def get_series(self):
        return [entry for entry in self._movies_list if isinstance(entry, Series)]

    def search(self):
        title = input("Podaj szukany tytuł ")
        watch_list = [entry.title for entry in self._movies_list if entry.title == title]
        print(watch_list)

    def generate_views(self):
        selected_movie = random.choice(self._movies_list)
        selected_movie.watch_amount += fake.random_int(0, 100)
        return selected_movie

    def top_titles(self):
        sorted_top_movies = sorted(self._movies_list, key=lambda best_movies: best_movies.watch_amount, reverse=True)
        sorted_top_movies_titles = [entry.title for entry in sorted_top_movies]
        best_movies = sorted_top_movies_titles[::3]
        print(best_movies)


if __name__ == '__main__':
    library = Library("test", [
        Movie(title="Mad Max 2", release_year="1981", genre="action", watch_amount=0),
        Movie(title="Die Hard", release_year="1988", genre="action", watch_amount=0),
        Movie(title="Castle in the Sky", release_year="1984", genre="animation", watch_amount=0),
        Movie(title="Blade Runner", release_year="1981", genre="action", watch_amount=0),
        Series(title="The Office", release_year="1982", genre="sitcom", episode_number="E01", season_number="S01",
               watch_amount=0),
        Series(title="Lucyfer", release_year="2013", genre="Comedy", episode_number="E03", season_number="S05",
               watch_amount=0),
        Series(title="South Park", release_year="2004", genre="animation", episode_number="E15", season_number="S02",
               watch_amount=0),
        Series(title="Teen Wolf", release_year="2016", genre="horror", episode_number="E01", season_number="S03",
               watch_amount=0),
        Series(title="Rick and Morty", release_year="2014", genre="animation", episode_number="E06",
               season_number="S06", watch_amount=0)
    ])

    library.print_all_movies()

    for _ in range(10):
        library.generate_views()

    print(f"Najpopularniejsze filmy i seriale dnia {d1}")
    library.top_titles()
