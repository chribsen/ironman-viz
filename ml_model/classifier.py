from scraper.database import init_db
from scraper.database import db_session
from scraper.models import Athlete
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor, BaggingRegressor
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier, BaggingClassifier

from sklearn.cross_validation import cross_val_score, train_test_split
import json

class AgePredictor:

    def __init__(self):
        self.X = []
        self.y = []

    def get_data(self):

        for each in Athlete.query.all():
            self.X.append([each.div_rank,each.gender_rank,each.overall_rank,each.swim_time,
                      each.bike_time,each.run_time,each.finish_time,each.points])

            self.y.append(each.age)

    def cross_validation(self):

        results = dict(randomforest=[], gradientboost=[], adaboost=[], bagging=[])

        for i in range(1, 200, 4):
            cls = RandomForestRegressor(n_estimators=i)
            scores = cross_val_score(cls, self.X, self.y, cv=7)
            results['randomforest'].append(dict(score=scores.mean(), estimators=i))

            cls = GradientBoostingRegressor(n_estimators=i)
            scores = cross_val_score(cls, self.X, self.y, cv=7)
            results['gradientboost'].append(dict(score=scores.mean(), estimators=i))

            cls = AdaBoostRegressor(n_estimators=i)
            scores = cross_val_score(cls, self.X, self.y, cv=7)
            results['adaboost'].append(dict(score=scores.mean(), estimators=i))

            cls = BaggingRegressor(n_estimators=i)
            scores = cross_val_score(cls, self.X, self.y, cv=7)
            results['bagging'].append(dict(score=scores.mean(), estimators=i))

            print(str(i))

        f = open('training-results.json', 'w+')
        f.write(json.dumps(results, indent=2))
        f.close()

    def train(self):
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=0)

        self.cls = GradientBoostingRegressor(n_estimators=17)
        self.cls = self.cls.fit(X_train, y_train)

        for x, y in zip(X_test, y_test):
            y_pred = self.cls.predict([x])
            print('pred: {0} - true: {1}'.format(str(y_pred), str(y)))




class ResultPredictor:

    def __init__(self):
        self.X = []
        self.y = []

    def get_data(self):

        for each in Athlete.query.all():
            self.X.append([each.swim_time, each.age])

            self.y.append(each.finish_time - (each.finish_time % 10))

    def cross_validation(self):

        results = dict(randomforest=[], gradientboost=[], adaboost=[], bagging=[])

        for x, i in enumerate(range(1, 200, 4)):
            cls = RandomForestClassifier(n_estimators=i)
            scores = cross_val_score(cls, self.X, self.y, cv=7)
            results['randomforest'].append(dict(score=scores.mean(), estimators=i))

            cls = GradientBoostingClassifier(n_estimators=i)
            scores = cross_val_score(cls, self.X, self.y, cv=7)
            results['gradientboost'].append(dict(score=scores.mean(), estimators=i))

            cls = AdaBoostClassifier(n_estimators=i)
            scores = cross_val_score(cls, self.X, self.y, cv=7)
            results['adaboost'].append(dict(score=scores.mean(), estimators=i))

            cls = BaggingClassifier(n_estimators=i)
            scores = cross_val_score(cls, self.X, self.y, cv=7)
            results['bagging'].append(dict(score=scores.mean(), estimators=i))

            print(str(i))

            for key in results.keys():
                print(key)
                print(results[key][x])


        f = open('training-results.json', 'w+')
        f.write(json.dumps(results, indent=2))
        f.close()

    def train(self):
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=0)

        self.cls = GradientBoostingRegressor(n_estimators=17)
        self.cls = self.cls.fit(X_train, y_train)

        for x, y in zip(X_test, y_test):
            y_pred = self.cls.predict([x])
            print('pred: {0} - true: {1}'.format(str(y_pred), str(y)))


a = ResultPredictor()
a.get_data()
a.cross_validation()
#a.train()