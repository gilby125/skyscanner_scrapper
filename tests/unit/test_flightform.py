# coding: utf-8

import datetime
from ..base import BaseTestCase
from scrapper.scrapper_blueprint.forms import FlightForm


form_valid_data = {'adults': u'1', 'outbound_date': datetime.date(2015, 1, 1), 'currency': u'BRL',
                   'flight_from': u'cwb', 'infants': u'0', 'inbound_date': datetime.date(2015, 2, 2), 'flight_to': u'edi',
                   'children': u'0', 'market': u'BR'}



class FlightFormTest(BaseTestCase):
    def setUp(self):
        '''
        This returns a valid form instance for each test case
        '''
        self.form = FlightForm(csrf_enabled=False, **form_valid_data)
        self.form.currency.choices = [('BRL', 'BRL'), ('GBP', 'GBP'), ('EUR', 'EUR')]
        self.form.market.choices = [('GB', 'GB'), ('BR', 'BR'), ('ES', 'ES')]
        
    def test_form_passes_validation(self):
        self.assertTrue(self.form.validate())

    def test_form_invalid_params(self):
        self.form['market'].data = 'XXX'
        self.assertFalse(self.form.validate())
        
    def test_optional_parameters(self):
        self.assertTrue(self.form.validate())
        
        self.form.inbound_date = None
        self.assertTrue(self.form.validate())
