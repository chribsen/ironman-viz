from flask import Flask, jsonify, request
from sqlalchemy import asc, desc
from scraper.database import db_session
from scraper.models import Athlete
from pyelasticsearch import ElasticSearch

app = Flask(__name__, static_url_path='')
es = ElasticSearch('http://localhost:9200/')

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/')
def index():
    return app.send_static_file('templates/index.html')

@app.route('/athletes')
def athletes():
    exclude = request.args.get('exclude')
    if exclude:
        exclude = exclude.split(',')

    athletes = [athlete.as_dict(exclude=exclude) for athlete in Athlete.query.order_by(asc(Athlete.overall_rank)).all()]
    return jsonify(dict(athletes=athletes))

@app.route('/search')
def search_athletes():
    q = request.args.get('q')

    if q:
        return jsonify(es.search({ "query": { "match_phrase_prefix": { "name": q}}}, index='athletes')['hits'])
    return jsonify(dict(result=None))


if __name__ == '__main__':
    app.run(debug=True)


