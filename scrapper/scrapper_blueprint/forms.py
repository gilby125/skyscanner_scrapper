# encoding: utf-8

from flask_wtf import Form
from wtforms import StringField, DateField, SelectField
from wtforms.validators import DataRequired, optional


class FlightForm(Form):
    market = SelectField('Country', validators=[DataRequired()])
    flight_from = StringField('Origin', validators=[DataRequired()])
    flight_to = StringField('Destination', validators=[DataRequired()])
    outbound_date = DateField('Departure Date', validators=[DataRequired()], id='outbound')
    inbound_date = DateField('Return Date', id='inbound', validators=[optional()])
    adults = SelectField('Adults', choices=[(str(i), str(i)) for i in range(1, 9)])
    children = SelectField('Children', choices=[(str(i), str(i)) for i in range(9)], validators=[optional()])
    infants = SelectField('Infants', choices=[(str(i), str(i)) for i in range(9)], validators=[optional()])
    currency = SelectField('Currency', validators=[DataRequired()])
