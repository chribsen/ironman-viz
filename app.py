from flask import Flask, jsonify, request
from scraper.database import db_session
from scraper.models import Athlete

app = Flask(__name__)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/athletes')
def athletes():
    exclude = request.args.get('exclude')
    if exclude:
        exclude = exclude.split(',')

    athletes = [athlete.as_dict(exclude=exclude) for athlete in Athlete.query.all()]
    return jsonify(dict(athletes=athletes))

if __name__ == '__main__':
    app.run()