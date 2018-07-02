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
    <form action="/picks" method="GET">
      <input type=text name=id>
         <input type=submit value=Get>
    </form>
</body>
</html>
"""


@application.route('/picks', methods=['GET'])
def redirect_picks():
    return flask.redirect('/picks/%s' % request.values['id'])
 

@application.route('/picks/<player_id>')
def get_picks(player_id):
    sample = request.args.get('sample')
    if not sample:
        sample = 75
    mode = request.args.get('mode')
    result = CONTROLLER.get_suggestions(player_id, sample, mode)
    if request.accept_mimetypes.accept_html:
        return flask.render_template('picks.html', picks=result['picks'], bans=result['bans'],
                                     avg=result['avg_win'], sample=result['sample'])
    elif request.accept_mimetypes.accept_json:
        return flask.jsonify(result)
    else:
        flask.abort(415)


if __name__ == '__main__':
        application.run()
