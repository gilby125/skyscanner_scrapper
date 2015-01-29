#!/usr/bin/env python
# encoding: utf-8

from flask import request, render_template
from flask.views import MethodView
from .skyscanner import Skyscanner
from .forms import FlightForm


class Scrapper(MethodView):
    def __init__(self, *args, **kwargs):
        self.api = Skyscanner()
        currencies = self.api.get_currency_list()
        locales = self.api.get_locale_list()
        self.locale = request.accept_languages.best_match(locales, default='en-GB')
        markets = self.api.get_market_list(self.locale)

        # TODO: In a real world app, the csrf token should be enabled
        self.form = FlightForm(csrf_enabled=False)
        self.form.currency.choices = currencies
        self.form.market.choices = markets

        super(MethodView, self).__init__(*args, **kwargs)

    def get(self):
        return render_template('index.html', form=self.form)

    def post(self):
        if not self.form.validate():
            # TODO: I should use flash messages here, but that would imply modifying more
            # stuff (like add a session key) and I have more important concerns right now
            message = 'Please check the information provided'
            return render_template('index.html', form=self.form, message=message)

        data = self.form.data
        data['locale'] = self.locale
        quotes = self.api.get_quotes(**data)

        if type(quotes) != dict:
            message = quotes
            return render_template('index.html', form=self.form, message=message)

        if not quotes['Itineraries']:
            # Sometimes the itineraries list is sent empty
            # I have no idea why, it may be a bug from Skyscanner
            # so we have to repeat the search
            quotes = self.api.get_quotes(**data)
            if type(quotes) != dict:
                message = quotes
                return render_template('index.html', form=self.form, message=message)


        legs = {leg['Id']: leg for leg in quotes['Legs']}
        places = {place['Id']: place for place in quotes['Places']}
        itineraries = quotes['Itineraries']
        currency = quotes['Currencies'][0]

        return render_template('index.html', form=self.form, itineraries=itineraries,
                               legs=legs, places=places, currency=currency)
