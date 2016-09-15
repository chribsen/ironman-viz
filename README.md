# Application for scraping and visualizing Iron Man 2016.

## Scraper: How to use
The scraper collects all athletes from the official Iron Man site into a list of `Athlete` objects.
The following command initiales the scraper
```
from models.web_scraper import IronManScraper
scraper = IronManScraper()
```

After the scraper has been initialized, the data will be fetched by issuing the following call
```
scraper.get_athletes()
```

At this point you can either access the data from the sqlite database at `sqlite:////tmp/athletes.db` or accessing the list of athletes as `scraper.athletes`

## API: How to use

The web application is built around an API. Although the API is pretty basic, it gives access to all the data necessary. The following HTTP GET returns all athletes:

```
curl -X GET "/athletes"
```

This call returns the following:
```
{
  "athletes": [
{
      "bike_time": 15255,
      "country": "SWE",
      "div_rank": 1,
      "finish_time": 28158,
      "gender_rank": 1,
      "id": 1,
      "name": "Patrik Nilsson",
      "overall_rank": 1,
      "points": 5000,
      "run_time": 9794,
      "swim_time": 2873
    },
    {
      "bike_time": 15873,
      "country": "GBR",
      "div_rank": 2,
      "finish_time": 28771,
      "gender_rank": 2,
      "id": 2,
      "name": "Will Clarke",
      "overall_rank": 2,
      "points": 4877,
      "run_time": 9796,
      "swim_time": 2866
    }
  ]
}  
```

We can limit this result by using the optional `exclude` query parameter specified on the endpoint:

```
curl -X GET "/athletes?exclude=bike_time,swim_time,points,finish_time"
```

This excludes the properties `bike_time`, `swim_time`, `points` and `finish_time`.

```
{
  "athletes": [
    {
      "country": "SWE",
      "div_rank": 1,
      "gender_rank": 1,
      "id": 1,
      "name": "Patrik Nilsson",
      "overall_rank": 1,
      "run_time": 9794
    },
    {
      "country": "GBR",
      "div_rank": 2,
      "gender_rank": 2,
      "id": 2,
      "name": "Will Clarke",
      "overall_rank": 2,
      "run_time": 9796
    }
  ]
}  
```

## Web app: How to use

The web application requires that elasticsearch is installed. When elasticsearch is up and running on localhost port `:9200`, change the path in `scraper/database.py` (it's absolute at the moment), make sure all pip dependencies are right and hit `python3 app.py`.