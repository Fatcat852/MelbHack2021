from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import Length, DataRequired, Email, ValidationError
from Fitnet.model import Users

class RegisterForm(FlaskForm):
    def validate_email_address(self, email_address_check):
        email = Users.query.filter_by(email_address=email_address_check.data).first()
        if email:
            raise ValidationError("Email already exists!")
    def validate_user_name(self, username_check):
        user = Users.query.filter_by(user_name=username_check.data).first()
        if user:
            raise ValidationError("Email already exists!")

    username = StringField(label='username', validators=[DataRequired(), Length(min=3, max=30)])
    email_address = StringField(label='email', validators=[DataRequired(), Length(min=3, max=30), Email()])
    password = PasswordField(label='password', validators=[DataRequired(), Length(min=6, max=50)])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    email_address = StringField(label='email', validators=[DataRequired(), Email()])
    password = PasswordField(label='password', validators=[DataRequired()])
    submit = SubmitField(label='Log in')

class RoutineForm(FlaskForm):
    name = StringField(label='name', validators=[DataRequired()])
    type = StringField(label='type', validators=[DataRequired()])
    duration = IntegerField(label='duration', validators=[DataRequired()])
    equipment = StringField(label='equipment')
    exercises = TextAreaField(label='exercises', validators=[DataRequired()])
    submit = SubmitField(label='Post')

class EmptyForm(FlaskForm):
    username = StringField(label='username', validators=[DataRequired(), Length(min=3, max=30)])
    submit = SubmitField('Add')
