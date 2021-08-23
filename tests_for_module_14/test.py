from unittest.mock import Mock
from main import app
import pytest


@pytest.mark.parametrize("list_type", ("now_playing", "popular", "upcoming", "top_rated"))
def test_homepage(monkeypatch, list_type):
    api_mock = Mock(return_value={'results': []})
    monkeypatch.setattr("tmdb_client.call_tmdb_api", api_mock)

    with app.test_client() as client:
        response = client.get(f'/movies/?list_type={list_type}')
        assert response.status_code == 200
        api_mock.assert_called_once_with(list_type)
