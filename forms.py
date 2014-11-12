__author__ = 'marcusfaust'

import re
from wtforms import Form, TextField, PasswordField, IntegerField, ValidationError
from wtforms.validators import Required, Email, EqualTo, NumberRange, Regexp

def valid_ip(form, field):
    if not re.match(r'^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$', field.data):
            raise ValidationError('Invalid IP Address')


class NewUserForm(Form):
    boxuseremail = TextField('Box Account Email', [Required(), Email(message='Invalid Email Address')])
    mitrend_user = TextField('MiTrend User Email', [Required(), Email(message='Invalid Email Address')])
    password = PasswordField('MiTrend Password', [Required(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password', [Required()])


class assignRU(Form):
    pass


class NodeIdentities(Form):
    starting_ip = TextField('First IP Address', [Required(), Regexp(r'^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$', message='Invalid IP Address')])
    hostname_prefix = TextField('Hostname Range Prefix', [Required()])
    first_hostname_id = TextField('First Hostname Identifier', [Required(), Regexp(r'^[0-9]*$', message='Invalid Integer')])
    count = IntegerField('Item Count', [Required(), NumberRange(min=1, max=60, message='Outside of Range')])

