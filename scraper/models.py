from sqlalchemy import Column, Integer, String
from scraper.database import Base

class Athlete(Base):
    __tablename__ = 'athletes'
    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    country = Column(String(10))
    div_rank = Column(Integer)
    gender_rank = Column(Integer)
    overall_rank = Column(Integer)
    swim_time = Column(Integer)
    bike_time = Column(Integer)
    run_time = Column(Integer)
    finish_time = Column(Integer)
    points = Column(Integer)

    def __init__(self, name=None, country=None, div_rank=None, gender_rank=None,
                 overall_rank=None, swim_time=None, bike_time=None, run_time=None,
                 finish_time=None, points=None):
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

    def as_dict(self, exclude=None):

        athlete = {c.name: getattr(self, c.name) for c in self.__table__.columns}

        # Excludes columns before returning the dictionary
        if exclude:
            for column in exclude:
                athlete.pop(column)

        return athlete

    def __repr__(self):
        return '<Athlete %r>' % (self.name)