from flask.views import MethodView
from flask_smorest import abort
from uuid import uuid4

from models import GameModel
from schemas import GamesSchema, GamesSchemaNested
from . import bp

@bp.route('/<games_id>')
class Games(MethodView):

    @bp.response(200, GamesSchemaNested)
    def get(self, games_id):
        game = GameModel.query.get(games_id)
        if game:
            print(game.author)
            return game
        abort(400, message='Invalid Game')

    @bp.arguments(GamesSchema)
    def put(self, games_data ,post_id):
        post = GameModel.query.get(post_id)
        if post:
            post.body = games_data['body']
            post.commit()   
            return {'message': 'post updated'}, 201
        return {'message': "Invalid Post Id"}, 400
    
    @bp.response(201, GamesSchema)
    def post(self, games_data):
        user_id = games_data['user_id']
        if user_id in users:
            game_id = uuid4()
            games[game_id] = games_data
            return {'message': "Game Created", 'game_id': str(game_id)}, 201
        abort(401, message='Invalid User')

    @bp.arguments(GamesSchema)
    def put(self, games_data, games_id):
        game = games.get(games_id)
        if game:
            if games_data['user_id'] == game['user_id']:
                game['body'] = games_data['body']
                return {'message': 'Game Updated'}, 202
            abort(401, message='Unauthorized')
        abort(400, message='Invalid Game')

    def delete(self, games_id):
        game = GameModel.query.get(games_id)
        if game:
            del games[games_id]
            return {"message": "Game Deleted"}, 202
        abort(400, message='Invalid Game')

@bp.route('/')
class GamesList(MethodView):

    @bp.response(200, GamesSchema(many=True))
    def get(self):
        return list(GameModel.query.all())

    @bp.arguments(GamesSchema)
    def post(self, games_data):
        user_id = games_data['user_id']
        if user_id in users:
            game_id = uuid4()
            games[game_id] = games_data
            return {'message': "Game Created", 'game_id': str(game_id)}, 201
        abort(401, message='Invalid User')
