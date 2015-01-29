#!/usr/bin/env python
# encoding: utf-8

import requests
from flask import current_app


class Skyscanner(object):
    def __init__(self, api_key=None, quote_url=None, currency_url=None, market_url=None, locale_url=None):
        self.api_key = api_key or current_app.config['API_KEY']
        self.quote_url = quote_url or current_app.config['QUOTE_URL']
        self.currency_url = currency_url or current_app.config['CURRENCY_URL']
        self.market_url = market_url or current_app.config['MARKET_URL']
        self.locale_url = locale_url or current_app.config['LOCALE_URL']
        
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}

    def get_quotes(self, market, locale, flight_from, flight_to, outbound_date,
                   currency, inbound_date, adults, children, infants):

        data = {'country': market, 'currency': currency, 'locale': locale, 'originplace': flight_from,
                'destinationplace': flight_to, 'outbounddate': outbound_date, 'inbounddate': inbound_date}

        data['apiKey'] = self.api_key
        data['originplace'] += '-sky'
        data['destinationplace'] += '-sky'

        if self.quote_url.endswith('v1.0'):
            # It means we don't have a token yet. Let's get one
            response = requests.post(self.quote_url, headers=self.headers, data=data)
            if response.status_code != 201:
                return 'Fail to get skyscanner token: {} {}'.format(response.reason, response.text)
            self.quote_url = response.headers['location']

        response = requests.get(self.quote_url, headers=self.headers, params=data)

        if response.status_code != 200:
            return 'Fail to communicate to skyscanner: {} {}'.format(response.reason, response.text)

        quotes = response.json()
        return quotes

    def get_currency_list(self):
        response = requests.get(self.currency_url, headers=self.headers, params={'apiKey': self.api_key})

        if response.status_code != 200:
            return response.reason

        currencies = response.json()
        currencies = currencies['Currencies']
        currencies = [(curr['Code'], u'{} - {}'.format(curr['Code'], curr['Symbol'])) for curr in currencies]

        return currencies

    def get_market_list(self, locale):
        response = requests.get(self.market_url.format(locale=locale),
                                headers=self.headers, params={'apiKey': self.api_key})

        if response.status_code != 200:
            return response.reason

        markets = response.json()
        markets = markets['Countries']
        markets = [(market['Code'], market['Name']) for market in markets]

        return markets

    def get_locale_list(self):
        response = requests.get(self.locale_url, headers=self.headers, params={'apiKey': self.api_key})

        if response.status_code != 200:
            return response.reason

        locales = response.json()
        locales = locales['Locales']
        locales = [local['Code'] for local in locales]
        return locales
