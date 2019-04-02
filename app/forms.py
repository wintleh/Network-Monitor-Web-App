from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired

class GraphForm(FlaskForm):
    nic = StringField('NIC', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    # TODO implement
    # timeInterval = StringField('Time Interval', validators=[DataRequired()])
    submit = SubmitField('Generate Graph')

class LibraryForm(FlaskForm):
    reset = SubmitField('Clear Graphs')


# Probably need a form for deleting the graphs
