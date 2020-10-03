import flask
from flask import Flask
from flask.globals import request
from statscontroller import StatsController
import hero
from flask.helpers import url_for
from json.encoder import JSONEncoder


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
                                  sortOrder=request.values['sort'],
                                  hero_id=request.values.get('heroPick'),
                                  query=request.values.get('query')))
 
 
class CustomEncoder(JSONEncoder):
    def default(self, obj):
        encoded = {}
        for attr in dir(obj):
            if not attr.startswith("_"):
                encoded[attr] = getattr(obj,attr)
        return encoded
 
application.json_encoder = CustomEncoder

@application.route('/<player_id>/suggestions')
def get_suggestions(player_id):
    try:
        controller = StatsController(player_id, request.args)
        result = controller.get_suggestions(request.args.get('sortOrder'), request.args.get('query'), request.args.get('hero_id'))
    except (TypeError):
        flask.abort(422)
    if request.headers.get('Content-Type') == 'application/json':
        return flask.jsonify(result)
    elif request.accept_mimetypes.accept_html:
        return flask.render_template('suggestions.html', result=result, id=player_id, mode=request.args.get('mode'),
                                     query=request.query_string.decode('UTF-8'))
    else:
        flask.abort(415)


@application.route('/suggestions')
def empty_suggestions():
    return flask.redirect(url_for('landing_page'))


@application.route('/<player_id>/synergies/<hero_id>')
def get_synergies(player_id, hero_id):
    try:
        controller = StatsController(player_id, request.args)
        with_result = controller.get_suggestions(request.args.get('sortOrder'), '&with_hero_id=', hero_id)

        against_result = controller.get_suggestions(request.args.get('sortOrder'), '&against_hero_id=', hero_id)
    except (TypeError):
        flask.abort(422)
    if request.accept_mimetypes.accept_html:
        return flask.render_template('synergies.html', with_result=with_result, against_result=against_result,
                                     id=player_id, synergy_id=hero_id, mode=request.args.get('mode'),
                                     query=request.query_string.decode('UTF-8'),
                                     heroes=sorted(hero.HERO_INFORMATION.values(), key=lambda x: x['localized_name']))
    else:
        flask.abort(415)


@application.route('/<player_id>/synergies/redirect')
def redirect_synergies(player_id):
    return flask.redirect(url_for('get_synergies',
                                  player_id=player_id,
                                  hero_id=request.values['synergy_id']) + '?' + request.values['query'])


@application.route('/heroes')
def get_heroes():
    return flask.jsonify(hero.HERO_INFORMATION)


if __name__ == '__main__':
        application.run()
        # application.send_static_file('istatic/pick.html')
