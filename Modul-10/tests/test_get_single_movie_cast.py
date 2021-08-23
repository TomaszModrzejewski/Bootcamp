import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tmdb_client
from unittest.mock import Mock


def test_get_single_movie_cast(monkeypatch):
    mock_single_movie_cast = [{"cast": "cast 1"}]
    mock_cast = mock_single_movie_cast[0]
    mock_cast_fin = mock_cast["cast"]
    requests_mock = Mock()
    response = requests_mock.return_value
    response.json.return_value = mock_cast
    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)
    single_movie_cast = tmdb_client.get_single_movie_cast(movie_id="123")
    assert single_movie_cast == mock_cast_fin
