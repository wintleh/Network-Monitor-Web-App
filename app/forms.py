from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class GraphForm(FlaskForm):
    nic = StringField('NIC', validators=[DataRequired()])
    time = StringField('Time', validators=[DataRequired()])
    timeInterval = StringField('Time Interval', validators=[DataRequired()])
    submit = SubmitField('Generate Graph')

class LibraryForm(FlaskForm):
    reset = SubmitField('Clear Graphs')


# Probably need a form for deleting the graphs
