import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app
from unittest.mock import Mock



def test_homepage(monkeypatch):
    api_mock = Mock(return_value={'results': []})
    monkeypatch.setattr("tmdb_client.get_movies_list", api_mock)

    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        api_mock.assert_called_once_with('popular')
