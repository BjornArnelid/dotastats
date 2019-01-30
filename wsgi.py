import flask
from flask import Flask
from flask.globals import request
from statscontroller import StatsController
from flask.helpers import url_for


application = Flask(__name__)


@application.route('/')
def landing_page():
    return flask.render_template('index.html', request=request.args)


@application.route('/redirect', methods=['GET'])
def redirect_picks():
    # Inform user if id is wrong
    return flask.redirect(url_for('get_suggestions',
                                  player_id=request.values['id'],
                                  sample=request.values['sample'],
                                  allies=request.values['allies'],
                                  mode=request.values['mode'],
                                  sortOrder=request.values['sort']))
 

@application.route('/<player_id>/suggestions')
def get_suggestions(player_id):
    try:
        controller = StatsController(player_id, request.args)
        result = controller.get_suggestions(request.args.get('sortOrder'))
    except (TypeError, ZeroDivisionError):
        flask.abort(422)
    if request.accept_mimetypes.accept_html:
        return flask.render_template('suggestions.html', result=result, id=player_id, mode=request.args.get('mode'), query=request.query_string.decode('UTF-8'))
    else:
        flask.abort(415)


@application.route('/suggestions')
def empty_suggestions():
    return flask.redirect(url_for('landing_page'))


@application.route('/<player_id>/counters/<hero_id>')
def get_counters(player_id, hero_id):
    try:
        controller = StatsController(player_id, request.args)
        result = controller.get_counter(hero_id, request.args.get('sortOrder'))
    except (TypeError, ZeroDivisionError):
        flask.abort(422)
    if request.accept_mimetypes.accept_html:
        return flask.render_template('counters.html', result=result, id=player_id, mode=request.args.get('mode'), query=request.query_string.decode('UTF-8'))
    else:
        flask.abort(415)


if __name__ == '__main__':
        application.run()
