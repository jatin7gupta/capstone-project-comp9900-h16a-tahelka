from flask import request, g
from flask_restx import Namespace, Resource
from werkzeug.exceptions import NotFound

from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.Subscription import Subscription
from models.Movie import Movie
from models.User import User
from models.WishList import Wishlist

api = Namespace('SubscribedWishlistMovies', path='/subscribedWishlistMovies')

@api.route('')
class SubscribedWishlistMovies(Resource):

    def get(self):
        '''
        Get wishlised movies of the users the current user is subscribed to.
        :return:
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        session = Session()

        cid = g.userID

        results = session.query(User.username, Movie.title, User.userID)\
                .select_from(Subscription)\
                .join(Wishlist, Wishlist.userID == Subscription.subscribedUserID)\
                .join(Movie, Movie.movieID == Wishlist.movieID)\
                .join(User, User.userID == Subscription.subscribedUserID)\
                .filter(Subscription.userID == cid)

        movies = list()
        for username, title, userID in results:
            movies.append({'userID': userID, 'username': username, 'title': title})

        response = {'movies':movies}
        return response, 200