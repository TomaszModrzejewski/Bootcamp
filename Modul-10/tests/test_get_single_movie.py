import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tmdb_client
from unittest.mock import Mock


def test_get_single_movie(monkeypatch):
    mock_single_movie = ['Movie 1']
    requests_mock = Mock()
    response = requests_mock.return_value
    response.json.return_value = mock_single_movie
    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)
    single_movie = tmdb_client.get_single_movie(movie_id="123")
    assert single_movie == mock_single_movie
