from flask import Flask
import flask
from statscontroller import StatsController
from flask.globals import request


CONTROLLER = StatsController()


application = Flask(__name__)


@application.route('/')
def hello_world():
    return 'Hello, World!'

 
@application.route('/picks/<player_id>')
def get_picks(player_id):
    result = CONTROLLER.get_suggestions(player_id)
    if request.accept_mimetypes.accept_html:
        return flask.render_template('picks.html', picks=result['picks'], bans=result['bans'])
    elif request.accept_mimetypes.accept_json:
        return flask.jsonify(result)
    else:
        flask.abort(415)


if __name__ == '__main__':
        application.run()
