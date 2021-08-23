from unittest import TestCase
from unittest.mock import patch
from . import tmdb_client


class TestTMDBClient(TestCase):

    def test_get_movies_list(self):
        with patch("library.tmdb_client.requests.get") as mock_get_movies_list:
            tmdb_client.get_movies_list('popular')

        self.assertEqual(mock_get_movies_list.called, True)

    def test_get_single_movies(self):
        with patch("library.tmdb_client.requests.get") as mock_get_movie:
            tmdb_client.get_single_movie('popular')

        self.assertEqual(mock_get_movie.called, True)

    def test_get_single_movie_cast(self):
        with patch("library.tmdb_client.requests.get") as mock_get_cast:
            tmdb_client.get_single_movie_cast('popular')

        self.assertEqual(mock_get_cast.called, True)

    def test_get_poster_url(self):
        movie_image = "https://image.tmdb.org/t/p/w780/86L8wqGMDbwURPni2t7FQ0nDjsH.jpg"
        image = tmdb_client.get_poster_url(
            "86L8wqGMDbwURPni2t7FQ0nDjsH.jpg", size="w780")

        self.assertEqual(image, movie_image)
