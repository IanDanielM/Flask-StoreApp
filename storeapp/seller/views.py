from flask import Blueprint,render_template,flash,redirect,url_for
from .forms import RegistrationForm
from storeapp.models import User
from storeapp import db
from storeapp.users.utils import send_confirmation_email


sellers = Blueprint('sellers', __name__)


@sellers.route('/seller/register',methods=['GET','POST'])
def sellerregister():
    form = RegistrationForm()
    if form.validate_on_submit():
        user=User(username=form.username.data,
                  email=form.email.data,
                  password=form.password.data,
                  address=form.address.data,
                  country=form.country.data,
                  town=form.town.data,
                  role='seller',
                  is_seller='true'
                  )
        db.session.add(user)
        db.session.commit()
        send_confirmation_email(user)
        flash(f'Account created for {form.username.data}! Check your email to confirm your account.', 'success')
        return redirect(url_for('users.login'))
    return render_template('seller/sellerregister.html',form=form)

@sellers.route('/seller/dashboard')
def dashboard():
    return render_template('seller/dashboard.html')



