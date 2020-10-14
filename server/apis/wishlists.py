from flask import request, g
from flask_restx import Namespace, fields, Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest

from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.WishList import Wishlist
from models.Movie import Movie
from models.User import User

api = Namespace('Wishlist', path='/wishlists',
                description='Add movies in Wishlist.')

wishlist_model = api.model('Wishlist', {
    'movieID': fields.Integer(description='Identifier of movie'),
})

@api.route('')
class Wishlists(Resource):

    @api.expect(wishlist_model)
    @api.response(201, "Movie added to Wishlist.")
    @api.response(400, "The parameters submitted are invalid.")
    def post(self):
        '''
            Adds a movie to the users' wishlist.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        movieID = request.json.get('movieID')

        new_wishlist = Wishlist(movieID, g.userID)
        session = Session()
        session.add(new_wishlist)
        try:
            session.commit()
        except IntegrityError:  #If wishlist already present
            session.rollback()
            raise BadRequest

        response = {'message':'Movie added to Wishlist.'}
        return response, 201

    def get(self):
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        session = Session()
        limit = 10
        results = session.query(Movie.movieID, Movie.title, Movie.year, Movie.ratings_sum, \
                               Movie.review_count) \
            .filter(Wishlist.userID == g.userID).filter(Wishlist.movieID == Movie.movieID) \
            .limit(limit)

        username = session.query(User.username).filter(User.userID == g.userID).first()
        movies = list()
        for movieID, title, year, ratings_sum, review_count in results:
            movies.append({'movieID': movieID, 'title': title, 'year': year,
                 'rating': ratings_sum / review_count if review_count else 0
                })

        response = {'username': username}
        response['Wishlist'] = movies

        return response, 200

