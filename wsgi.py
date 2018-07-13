import flask
from flask import Flask
from flask.globals import request
from statscontroller import StatsController
from flask.helpers import url_for


CONTROLLER = StatsController()
application = Flask(__name__)


@application.route('/')
def landing_page():
    player_id = request.args.get('id')
    if not player_id:
        player_id = ''
    return flask.render_template('index.html', id=player_id)


@application.route('/picks', methods=['GET'])
def redirect_picks():
    return flask.redirect(url_for('get_picks', player_id=request.values['id'], mode=request.values['mode']))
 

@application.route('/picks/<player_id>')
def get_picks(player_id):
    sample = request.args.get('sample')
    if not sample:
        sample = 75
    mode = request.args.get('mode')
    result = CONTROLLER.get_suggestions(player_id, sample, mode)
    if request.accept_mimetypes.accept_html:
        return flask.render_template('picks.html', result=result, id=player_id)
    elif request.accept_mimetypes.accept_json:
        return flask.jsonify(result)
    else:
        flask.abort(415)


if __name__ == '__main__':
        application.run()
