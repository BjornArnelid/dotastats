from flask import Flask
import flask
from statscontroller import StatsController


CONTROLLER = StatsController()


application = Flask(__name__)


@application.route('/')
def hello_world():
    return 'Hello, World!'


@application.route('/picks/<player_id>')
def get_picks(player_id):
    return flask.jsonify(CONTROLLER.get_suggestions(player_id))


if __name__ == '__main__':
        application.run()
