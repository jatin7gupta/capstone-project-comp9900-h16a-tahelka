from flask import current_app
import jwt
import time

class TokenGenerator:
    def __init__(self, filmfinder):
        self.filmfinder = filmfinder

    def generate(self):
        payload = self.construct_payload()
        secret = current_app.config['JWT_SECRET']
        return jwt.encode(payload, secret, algorithm='HS256').decode()

    def construct_payload(self):
        payload = {
            'id': self.filmfinder.id,
            'username': self.filmfinder.username,
            'email': self.filmfinder.email,
            'exp': TokenGenerator.decide_expire_time()
        }

        return payload

    def decide_expire_time():
        # Expire in 24 hours
        return int(time.time()) + (60 * 60 * 24)
