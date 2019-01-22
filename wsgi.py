import flask
from flask import Flask
from flask.globals import request
from statscontroller import StatsController
from flask.helpers import url_for


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
    try:
        controller = StatsController(player_id, request.args)
        result = controller.get_suggestions(request.args.get('sortOrder'))
        if request.accept_mimetypes.accept_html:
            return flask.render_template('picks.html', result=result, id=player_id, mode=request.args['mode'], query=request.query_string.decode('UTF-8'))
        else:
            flask.abort(415)
    except TypeError:
        flask.abort(400)


@application.route('/picks/<player_id>/counterpicks/<hero_id>')
def get_counters(player_id, hero_id):
    sample = request.args.get('sample')
    mode = request.args.get('mode')
    sort_order = request.args.get('sortOrder')
    allies = request.args.get('allies')
    try:
        controller = StatsController(player_id, request.args)
        result = controller.get_counter(hero_id, sort_order)
        result['mode'] = mode
        if request.accept_mimetypes.accept_html:
            return flask.render_template('counters.html', result=result, id=player_id, mode=request.args['mode'], query=request.query_string.decode('UTF-8'))
        else:
            flask.abort(415)
    except TypeError:
        flask.abort(400)


if __name__ == '__main__':
        application.run()
