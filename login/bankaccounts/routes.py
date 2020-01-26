from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from login import db
from login.models import BankAccount
from login.bankaccounts.forms import AddBankAccountForm

bankaccounts = Blueprint('bankaccounts',__name__)

@bankaccounts.route('/addbankaccount',methods=['GET','POST'])
@login_required
def addbankaccount():
    form  = AddBankAccountForm()
    if form.validate_on_submit():
        bankAccount = BankAccount(bank_account_no=form.bank_account_no.data,routing_number=form.routing_number.data,user_id=current_user.id,amount=form.amount.data)
        db.session.add(bankAccount)
        db.session.commit()
        flash('Your Bank Account has been added to your account','success')
        return redirect(url_for('main.home'))
    return render_template('addbankaccount.html',title='Add Bank Account',form=form,legend = 'Add new bank Account')
