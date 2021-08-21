import os
import sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app
from unittest.mock import Mock


@pytest.mark.parametrize('n, result', (
    ('popular', 200),
    ('now_playing', 200),
    ('top_rated', 200),
    ('upcoming', 200),
))
def test_homepage(monkeypatch, n, result):
    api_mock = Mock(return_value={'results': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]})
    monkeypatch.setattr("tmdb_client.get_movies_list", api_mock)

    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == result
