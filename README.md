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

At this point you can either persist the athlete data by calling `scraper.save_to_file()` or accessing the list of athletes as `scraper.athletes`
