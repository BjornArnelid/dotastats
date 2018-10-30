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
    return flask.redirect(url_for('get_picks',
                                  player_id=request.values['id'],
                                  sample=request.values['sample'],
                                  allies=request.values['allies'],
                                  mode=request.values['mode'],
                                  sortOrder=request.values['sort']))
 

@application.route('/picks/<player_id>')
def get_picks(player_id):
    sample = request.args.get('sample')
    mode = request.args.get('mode')
    sort_order = request.args.get('sortOrder')
    allies = request.args.get('allies')
    try:
        result = CONTROLLER.get_suggestions(player_id, sample, mode, sort_order, allies)
        result['mode'] = mode
    except TypeError:
        flask.abort(400)
    if request.accept_mimetypes.accept_html:
        return flask.render_template('picks.html', result=result, id=player_id)
    else:
        flask.abort(415)


if __name__ == '__main__':
        application.run()
