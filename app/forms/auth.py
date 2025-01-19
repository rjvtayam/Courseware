from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired

class TermsAgreementForm(FlaskForm):
    """Form for agreeing to terms and conditions"""
    agree_terms = BooleanField('I agree to the Terms of Service and Privacy Policy', 
                             validators=[DataRequired(message='You must agree to the terms to continue')])
    submit = SubmitField('Continue')