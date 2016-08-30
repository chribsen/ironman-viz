from bs4 import BeautifulSoup
import requests
import unittest
import pickle


class Athlete(object):

    def __init__(self, name, country, div_rank, gender_rank, overall_rank,
                 swim_time, bike_time, run_time, finish_time, points):
        self.name = self.__rearrange_name__(name)
        self.country = country
        self.div_rank = int(div_rank)
        self.gender_rank = int(gender_rank)
        self.overall_rank = int(overall_rank)
        self.swim_time = self.__reformat_time__(swim_time)
        self.bike_time = self.__reformat_time__(bike_time)
        self.run_time = self.__reformat_time__(run_time)
        self.finish_time = self.__reformat_time__(finish_time)
        self.points = int(points)

    def __rearrange_name__(self, name):
        """
        Rearranges a name from Danielsen, Christian to Christian Danielsen
        """
        split = [x.strip() for x in name.split(',')]
        split.reverse()
        return ' '.join(split)

    def __reformat_time__(self, time):
        """
        Takes a time like 01:23:22 and parses it to seconds
        """
        time_split = time.split(':')
        seconds = int(time_split[0])*60*60 + int(time_split[1])*60 + int(time_split[2])
        return seconds

class IronManScraper:

    def __init__(self):
        self.base_url = 'http://eu.ironman.com'
        self.endpoint = '/triathlon/events/emea/ironman/copenhagen/results.aspx?p={page}&ps=20#axzz4Iia1G5jw'
        self.get_endpoint = lambda page_number: self.base_url + self.endpoint.format(page=page_number)
        self.atheletes = []
        self.invalid_athelete_count = 0

    def get_athletes(self):
        for page_number in range(1, 142):
            print('Getting page {0}'.format(str(page_number)))
            r = requests.get(self.get_endpoint(page_number))
            self.atheletes += tuple(self.__parse_html__(r.text))

    def __parse_html__(self, html):
        rows = BeautifulSoup(html) \
            .find('table', {'class': 'tablesorter'}) \
            .find('tbody') \
            .find_all('tr')

        for row in rows:
            column_data = [ele.text.strip() for ele in row.find_all('td')]

            try:
                yield Athlete(
                    name=column_data[0],
                    country=column_data[1],
                    div_rank=column_data[2],
                    gender_rank=column_data[3],
                    overall_rank=column_data[4],
                    swim_time=column_data[5],
                    bike_time=column_data[6],
                    run_time=column_data[7],
                    finish_time=column_data[8],
                    points=column_data[9]
                )
            except ValueError as e:
                self.invalid_athelete_count += 1
                print('Invalid atheletes: {0}'.format(str(self.invalid_athelete_count)))
                continue

    def save_to_file(self, filename="athletes.pickle"):
        pickle.dump(self.atheletes, open(filename, "wb"))


class IronManScraperTest(unittest.TestCase):

    def test_parse_html(self):
        scraper = IronManScraper()
        scraper.get_athletes()
        scraper.save_to_file()
