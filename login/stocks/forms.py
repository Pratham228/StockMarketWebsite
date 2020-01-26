from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, Form, FieldList, FieldList
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from login.models import BuyStocks, BankAccount, Stock, UserStocks

class StockForm(Form):
    ticker_symbol= StringField('Ticker Symbol', validators=[DataRequired()])
    no_of_stocks= IntegerField('Number of stocks', validators=[DataRequired()])

class BuyStocksForm(FlaskForm):
    
    ticker_symbol= StringField('Ticker Symbol', validators=[DataRequired()])
    def choice_query() :
        return BankAccount.query.filter_by(user_id=current_user.id)
    bank_account_no = QuerySelectField(query_factory=choice_query,allow_blank=False,get_label='bank_account_no',validators=[DataRequired()])
    no_of_stocks= IntegerField('Number of stocks', validators=[DataRequired()])
    submit = SubmitField('Buy')
    
    def validate_ticker_symbol(self,ticker_symbol):
        buy_stocks = BuyStocks.query.filter_by(ticker_symbol=ticker_symbol.data).first()
        if buy_stocks is None:
            raise ValidationError('No such stock exists!')
    
    def validate_bank_account_no(self,bank_account_no):
        bank_account_no = BankAccount.query.filter_by(bank_account_no=bank_account_no.data.bank_account_no, user_id=current_user.id).first()
        stock = Stock.query.filter_by(ticker_symbol=self.ticker_symbol.data).first()
        new_amount = (bank_account_no.amount - (stock.price * self.no_of_stocks.data))
        if new_amount < 0 :
            raise ValidationError('Not enough balance in this account!')

class SellStocksForm(FlaskForm):
    ticker_symbol= StringField('Ticker Symbol', validators=[DataRequired()])
    def choice_query() :
        return BankAccount.query.filter_by(user_id=current_user.id)
    bank_account_no = QuerySelectField(query_factory=choice_query,allow_blank=False,get_label='bank_account_no',validators=[DataRequired()])
    # bank_account_no = StringField('Select Bank Account for payment', validators=[DataRequired()])
    no_of_stocks= IntegerField('Number of stocks', validators=[DataRequired()])
    submit = SubmitField('Sell')
    
    def validate_ticker_symbol(self,ticker_symbol):
        buy_stocks = BuyStocks.query.filter_by(ticker_symbol=ticker_symbol.data).first()
        if buy_stocks is None:
            raise ValidationError('No such stock exists!')
    
    def validate_bank_account_no(self,bank_account_no):
        bank_account_no = BankAccount.query.filter_by(bank_account_no=bank_account_no.data.bank_account_no, user_id=current_user.id).first()
        if bank_account_no is None:
            raise ValidationError('No such account linked to your account! Please add the bank account first.')
    
    def validate_no_of_stocks(self,no_of_stocks):
        user_stocks = UserStocks.query.filter_by(ticker_symbol=self.ticker_symbol.data, user_id=current_user.id).first()
        new_no_of_stocks = (user_stocks.no_of_stocks - no_of_stocks.data)
        if new_no_of_stocks < 0:
            raise ValidationError('You dont own these many of this particular stock!')
    
class TransferMoneyForm(FlaskForm):
    def choice_query() :
        return BankAccount.query.filter_by(user_id=current_user.id)
    bank_account_no1 = QuerySelectField(query_factory=choice_query,allow_blank=True,get_label='bank_account_no',validators=[DataRequired()])
    bank_account_no2 = QuerySelectField(query_factory=choice_query,allow_blank=True,get_label='bank_account_no',validators=[DataRequired()])
    amount_to_transfer = IntegerField('Amount to be transferred', validators=[DataRequired()])
    submit = SubmitField('Transfer')

    def validate_bank_account_no1(self,bank_account_no1):
        bank_account = BankAccount.query.filter_by(bank_account_no = bank_account_no1.data.bank_account_no).first()
        if bank_account.amount <  self.amount_to_transfer.data:
            raise ValidationError('Not enough balance in this account!')

    def validate_bank_account_no2(self,bank_account_no2):
        if bank_account_no2.data.bank_account_no ==  self.bank_account_no1.data.bank_account_no:
            raise ValidationError('Both account numbers are the same! Please provide different ones.')


class PlanScheduleForm(FlaskForm):
    def choice_query() :
        return BankAccount.query.filter_by(user_id=current_user.id)
    ticker_symbol= StringField('Ticker Symbol', validators=[DataRequired()])
    day = StringField('Day',validators=[DataRequired()])    
    bank_account_no = QuerySelectField(query_factory=choice_query,allow_blank=True,get_label='bank_account_no',validators=[DataRequired()])
    # bank_account_no = StringField('Select Bank Account for payment', validators=[DataRequired()])
    no_of_stocks= IntegerField('Number of stocks', validators=[DataRequired()])
    submit = SubmitField('Set')
    
    def validate_ticker_symbol(self,ticker_symbol):
        buy_stocks = BuyStocks.query.filter_by(ticker_symbol=ticker_symbol.data).first()
        if buy_stocks is None:
            raise ValidationError('No such stock exists!')
    
    def validate_bank_account_no(self,bank_account_no):
        bank_account_no = BankAccount.query.filter_by(bank_account_no=bank_account_no.data.bank_account_no, user_id=current_user.id).first()
        if bank_account_no is None:
            raise ValidationError('No such account linked to your account! Please add the bank account first.')
    
    def validate_no_of_stocks(self,no_of_stocks):
        user_stocks = UserStocks.query.filter_by(ticker_symbol=self.ticker_symbol.data, user_id=current_user.id).first()
        new_no_of_stocks = (user_stocks.no_of_stocks - no_of_stocks.data)
        if new_no_of_stocks < 0:
            raise ValidationError('You dont own these many of this particular stock!')
