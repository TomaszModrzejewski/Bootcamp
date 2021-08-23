from . import app, TestCase, patch, Mock


class TestLibrary(TestCase):

    def test_homepage(self):
        with patch("library.tmdb_client.get_movies") as mock_movie:
            mock_movie.return_value = {'results': list()}

            with app.test_client() as client:
                response = client.get('/')
                assert response.status_code == 200
                mock_movie.assert_called_once_with(8, 'popular')
