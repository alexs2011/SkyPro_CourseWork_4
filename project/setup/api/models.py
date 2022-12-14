from flask_restx import fields, Model

from project.setup.api import api

genre: Model = api.model('Жанр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Комедия'),
})

director: Model = api.model('Режиссер', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Тарантино'),
})

movie: Model = api.model('Фильм', {
    'id': fields.Integer(required=True, example=1),
    'title': fields.String(required=True, max_length=255, example=''),
    'description': fields.String(required=True, max_length=255, example=''),
    'trailer': fields.String(required=True, max_length=255, example=''),
    'year': fields.Integer(required=True, example=2019),
    'rating': fields.Float(required=True, example=1.2),
    'genre': fields.Nested(genre),
    'director': fields.Nested(director),
})

user: Model = api.model('Пользователь', {
    'id': fields.Integer(required=True, example=1),
    'email': fields.String(required=True, max_length=100, example=''),
    'password': fields.String(required=True, max_length=100, example=''),
    'name': fields.String(required=True, max_length=255, example=''),
    'surname': fields.String(required=True, max_length=255, example=''),
    'genre': fields.Nested(genre),
})
