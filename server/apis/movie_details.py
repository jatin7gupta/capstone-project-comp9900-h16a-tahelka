from db_engine import Session
from flask import request
from flask_restx import Namespace, fields, Resource
from authentication.token_authenticator import TokenAuthenticator
from models.FilmCast import FilmCast
from models.FilmDirector import FilmDirector
from models.GenreOfFilm import GenreOfFilm
from models.Genres import Genres
from models.Movie import Movie
from models.MovieReview import MovieReview
from models.Person import Person
from models.User import User
from werkzeug.exceptions import NotFound


api = Namespace('Movie Details', path = '/movies')

movie_review = api.model('Movie Review',
                         {'userID': fields.Integer,
                          'username': fields.String(description = 'The FilmFinder that left this review'),
                          'rating': fields.Float(description = 'A rating out of 5'),
                          'review': fields.String(description = "The FilmFinder's review of the movie")
                         }
                        )

movie_recommendation = api.model('Movie Recommendation',
                                 {'movieID': fields.Integer,
                                  'title': fields.String,
                                  'year': fields.Integer
                                 }
                                )

movie_details = api.model('Full Movie Details',
                          {'title': fields.String,
                           'year': fields.Integer,
                           'description': fields.String,
                           'genre': fields.List(fields.String),
                           'director': fields.List(fields.String),
                           'cast': fields.List(fields.String),
                           'rating': fields.Float(description = 'Average rating out of 5'),
                           'reviews': fields.List(fields.Nested(movie_review)),
                           'recommendations': fields.List(fields.Nested(movie_recommendation))
                          }
                         )

@api.route('/<int:id>')
@api.response(200, 'Success', movie_details)
@api.response(404, 'Movie was not found')
class MovieDetails(Resource):
    def get(self, id):
        '''
        View a movie's full details.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        session = Session()
        movie = session.query(Movie.movieID, Movie.title, Movie.year,
                              Movie.description, Movie.avg_rating
                             ).filter(Movie.movieID == id).one_or_none()
        if movie is None:
            raise NotFound
        genres = session.query(Genres.genre).join(GenreOfFilm)\
                                            .filter(GenreOfFilm.movieID == movie.movieID)
        genres = [genre for genre, in genres]
        directors = session.query(Person.name).join(FilmDirector)\
                                              .filter(FilmDirector.movieID == movie.movieID)
        directors = [director for director, in directors]
        cast = session.query(Person.name).join(FilmCast)\
                                         .filter(FilmCast.movieID == movie.movieID)
        cast = [member for member, in cast]
        reviews = session.query(User.userID, User.username,
                                MovieReview.rating, MovieReview.review
                               ).join(MovieReview)\
                                .filter(MovieReview.movieID == movie.movieID)
        reviews = [{'userID': userID, 'username': username,
                    'rating': rating, 'review': review
                   } for userID, username, rating, review in reviews
                  ]
        recommendations = []
        return {'title': movie.title, 'year': movie.year,
                'description': movie.description, 'genre': genres,
                'director': directors, 'cast': cast, 'rating': movie.avg_rating,
                'reviews': reviews, 'recommendations': recommendations
               }, 200
