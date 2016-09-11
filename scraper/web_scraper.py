from bs4 import BeautifulSoup
import requests, unittest
from scraper.database import init_db
from scraper.database import db_session
from scraper.models import Athlete


class IronManScraper:

    def __init__(self):
        self.base_url = 'http://eu.ironman.com/triathlon/events/emea/ironman/copenhagen/results.aspx'
        self.endpoint = '?p={page}&ps=20#axzz4Iia1G5jw'
        self.get_endpoint = lambda page_number: self.base_url + self.endpoint.format(page=page_number)
        self.atheletes = []
        self.invalid_athlete_count = 0

    def get_athletes(self):
        for page_number in range(1, 142):
            print('Getting page {0}'.format(str(page_number)))
            r = requests.get(self.get_endpoint(page_number))
            self.atheletes += tuple(self.__parse_html__(r.text))

        return self.atheletes

    def __get_profile__(self, endpoint):
        r = requests.get(self.base_url + endpoint)
        return r.text

    def __parse_html__(self, html):
        rows = BeautifulSoup(html) \
            .find('table', {'class': 'tablesorter'}) \
            .find('tbody') \
            .find_all('tr')

        endpoint = rows[0].find_all('a')[0]['href']
        profile_html = BeautifulSoup(self.__get_profile__(endpoint))

        profile_data = [td.text for td in profile_html.find_all('table', {'id': 'general-info'})[0].find_all('td')]


        for row in rows:
            column_data = [ele.text.strip() for ele in row.find_all('td')]

            try:
                athlete = Athlete(
                    name=column_data[0],
                    country=column_data[1],
                    div_rank=column_data[2],
                    gender_rank=column_data[3],
                    overall_rank=column_data[4],
                    swim_time=column_data[5],
                    bike_time=column_data[6],
                    run_time=column_data[7],
                    finish_time=column_data[8],
                    points=column_data[9],
                    bib_id=profile_data[2],
                    age=profile_data[6],
                    state=profile_data[8],
                    profession=profile_data[12]
                )
                db_session.add(athlete)
                db_session.commit()
                yield athlete

            except ValueError as e:
                self.invalid_athlete_count += 1
                print('Invalid atheletes: {0}'.format(str(self.invalid_athlete_count)))
                continue


class IronManScraperTest(unittest.TestCase):

    def test_parse_html(self):
        init_db()
        scraper = IronManScraper()
        scraper.get_athletes()
        db_session.remove()

    def test_get_data(self):
        print(Athlete.query.all())
        self.assertIsNotNone(Athlete.query.all())

        print(Athlete.query.filter(Athlete.name == 'Mark Johnston').first().age)
        self.assertIsNotNone(Athlete.query.filter(Athlete.name == 'Mark Johnston').first())

