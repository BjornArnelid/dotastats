import flask
from flask import Flask
from flask.globals import request
from statscontroller import StatsController


CONTROLLER = StatsController()
application = Flask(__name__)


@application.route('/')
def landing_page():
    # we'''
    return """
<head>
  <title>Choose hero</title>
</head>
<body>
    <form action="/picks/redirect">
      <p><input type=text name=id>
         <input type=submit value=Kör>
    </form>
</body>
</html>
"""

# Should allow post
@application.route('/picks/redirect', methods=['POST'])
def redirect_picks():
    return flask.redirect('/picks/%s' % request.form['id'])


@application.route('/picks/<player_id>')
def get_picks(player_id):
    if request.args.get('sample'):
        sample = request.args['sample']
    else:
        sample=50
    result = CONTROLLER.get_suggestions(player_id, sample)
    if request.accept_mimetypes.accept_html:
        return flask.render_template('picks.html', picks=result['picks'], bans=result['bans'],
                                     avg=result['avg_win'], sample=result['sample'])
    elif request.accept_mimetypes.accept_json:
        return flask.jsonify(result)
    else:
        flask.abort(415)


if __name__ == '__main__':
        application.run()
