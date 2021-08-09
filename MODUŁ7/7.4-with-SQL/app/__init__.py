import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Flask
app = Flask(__name__)
app.config["SECRET_KEY"] = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhMzY5N2Y1OWRlYzM1NGU4OWQ0Y2I0OWQ0NzRlYjc5ZCIsInN1YiI6IjYwZTY1Y2QwNmJkZWMzMDA0NjE3ODRjMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.fyxbWBx2Eqn5SRr1OnfF2ti8Kuec1TGOATYOcLdBmUI"
from app import views
