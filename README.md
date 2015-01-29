## Skyscanner scrapper

#### Installing dependencies

```
pip install -r requirements.txt
```

#### Usage

**As a web app**

`./manage.py runserver`

Then browser to `127.0.0.1:5000`

**As an api abstraction to Skyscanner**

From a python shell:

```
from scrapper.scrapper_blueprint.skyscanner import Skyscanner
api = Skyscanner(api_key, quote_url, currency_url, market_url, locale_url)
```

The class in `scrapper/scrapper_blueprint/Skyscanner.py` could also be easily modified into
(or used to build) a command line tool.

#### Tests and metrics

In order to test the software, run `nosetests`. There are only 3 tests, assuring the
correct behaviour of the form.

No tests for the web controllers were written because, unless mock was used, that would stress
an already limited api (as described bellow).

To run pylint and flake8 on the code, run:
`./manage.py lint`


#### Known issues and limitations

- The Skyscanner api only allow a couple requests per minute, and that could cause a problem. In that case
    a error message will be displayed instead of a search result

- The Skyscanner prediction tool for countries/cities/airports names was not used. So the software demands a
    real airport name to be typed as input

- It wasn't clear which information about the flight was mandatory for the task, so it was kept to a minimum,
    presenting only flight origin, destination, departure and arrival times, number of stops, price, and a link
    to the partner corresponding to that ticket. However, all the details about the flight is fetched from
    Skyscanner, so it should be easy to present more information on the screen.

