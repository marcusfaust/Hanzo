__author__ = 'marcusfaust'

from wtforms import Form, TextField, PasswordField, IntegerField
from wtforms.validators import Required, Email, EqualTo, NumberRange


class NewUserForm(Form):
    boxuseremail = TextField('Box Account Email', [Required(), Email(message='Invalid Email Address')])
    mitrend_user = TextField('MiTrend User Email', [Required(), Email(message='Invalid Email Address')])
    password = PasswordField('MiTrend Password', [Required(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password', [Required()])


class assignRU(Form):
    pass


class NodeIdentities(Form):
    starting_ip = TextField('IPv4 Range Prefix', [Required()])
    hostname_prefix = TextField('Hostname Range Prefix', [Required()])
    count = IntegerField('Item Count', [Required(), IntegerField(min=1, max=60, message='Invalid Integer')])

