import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tmdb_client
from unittest.mock import Mock


def test_get_movie_images(monkeypatch):
    mock_movie_images = ['Image 1', 'Image 2']
    requests_mock = Mock()
    response = requests_mock.return_value
    response.json.return_value = mock_movie_images
    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)
    movie_images = tmdb_client.get_movie_images(movie_id="123")
    assert movie_images == mock_movie_images
