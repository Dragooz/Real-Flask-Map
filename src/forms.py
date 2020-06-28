from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired


class RouteForm(FlaskForm):
    def validate(self):
        if self.route.data == 'None':
            return False
        return True

    route = SelectField('Routes', validators=[DataRequired()])
    submit = SubmitField("Search")
