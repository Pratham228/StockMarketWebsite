from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired,ValidationError
from login.models import BankAccount


class AddBankAccountForm(FlaskForm):
    bank_account_no = StringField('Bank Account Number',validators=[DataRequired()])
    routing_number = StringField('Rounting Number',validators=[DataRequired()])
    amount = IntegerField('Amount',validators=[DataRequired()])
    submit = SubmitField('Add Account')

    def validate_bank_account_no(self,bank_account_no):
        bank_account_no = BankAccount.query.filter_by(bank_account_no=bank_account_no.data).first()
        if bank_account_no:
            raise ValidationError('This account number is already registered')
