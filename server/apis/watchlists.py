from flask import request, g
from flask_restx import Namespace, fields, Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest

from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.Watchlist import Watchlist
from models.Movie import Movie

from util.IntValidations import is_valid_integer
from util.RatingCalculator import compute

api = Namespace('Watchlist', path='/watchlists',
                description='CRUD on Watchlist movies')

watchlist_model = api.model('Watchlist', {
    'movieID': fields.Integer(description='Identifier of movie'),
})

film_summary = api.model('Film Summary',
                         {'movieID': fields.Integer,
                          'title': fields.String,
                          'year': fields.Integer,
                          'rating': fields.String(description = 'Average rating out of 5')
                         }
                        )

movies_list = api.model('list',
                        {
                            'watchlist': fields.List(fields.Nested(film_summary))
                        })
@api.route('')
class Watchlists(Resource):

    @api.expect(watchlist_model)
    @api.response(201, "Movie added to Watchlist.")
    @api.response(400, "The parameters submitted are invalid.")
    @api.response(401, 'Authentication token is missing')
    def post(self):
        '''
            Adds a movie to the users' Watchlist.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        movieID = request.json.get('movieID')

        is_valid_integer(movieID)

        new_watchlist = Watchlist(movieID, g.userID)
        session = Session()
        session.add(new_watchlist)
        try:
            session.commit()
            session.close()
        except IntegrityError:  #If Watchlist already present
            session.rollback()
            raise BadRequest

        response = {'message':'Movie added to Watchlist.'}
        return response, 201

    @api.response(200, "Movies in user's Watchlist.", movies_list)
    @api.response(401, 'Authentication token is missing')
    @api.response(404, "User not found")
    def get(self):
        '''
        View list of movies in user's Watchlist
        :return:
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        session = Session()
        userID = g.userID

        is_valid_integer(userID)


        results = session.query(Movie.movieID, Movie.title, Movie.year, Movie.ratings_sum, \
                                Movie.review_count).filter(Watchlist.userID == userID) \
            .filter(Watchlist.movieID == Movie.movieID)

        movies = list()
        for movieID, title, year, ratings_sum, review_count in results:
            movies.append({'movieID': movieID, 'title': title, 'year': year,
                           'rating': str(compute(movieID, userID, ratings_sum, review_count))
                           })

        response = {'watchlist': movies}
        return response, 200
