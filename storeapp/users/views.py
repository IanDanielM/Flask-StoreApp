from flask import Blueprint,render_template,url_for,redirect,request,flash
from storeapp.models import User
from .forms import RegistrationForm,LoginForm,ConfirmForm,RequestResetForm,ResetPasswordForm,AccountEditForm
from storeapp import db
from flask_login import login_user,current_user,logout_user,login_required
from .utils import send_confirmation_email,send_reset_email,save_picture
users = Blueprint('users',__name__)

@users.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user=User(username=form.username.data,email=form.email.data,password=form.password.data,address=form.address.data,country=form.country.data,town=form.town.data)
        db.session.add(user)
        db.session.commit()
        send_confirmation_email(user)
        flash(f'Account created for {form.username.data}! Check your email to confirm your account.', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/register.html',form=form)

@users.route('/confirm', methods=['GET', 'POST'])
def confirm():
    if current_user.is_authenticated and current_user.confirmed: # type: ignore
        return redirect(url_for('login'))
    form=ConfirmForm()
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            if user.confirmed:
                flash('Your account has already been confirmed. Please log in.')
                return redirect(url_for('login'))
            else:
                send_confirmation_email(user)
                flash('A confirmation email has been sent to your email address. Please check your inbox and follow the instructions to confirm your account.')
                return redirect(url_for('users.login'))
        else:
            flash('Invalid email address. Please try again.')

    return render_template('users/confirm.html', form=form)


@users.route('/confirm_mail/<token>')
def confirm_mail(token):
    user = User.verify_confirm_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.login'))
    else:
        user.confirmed = True
        db.session.commit()
        flash('Your account has been confirmed! You are now able to log in.', 'success')
        return redirect(url_for('users.login'))
    
@users.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page) if next_page else redirect(url_for('main.index'))
            flash('You have been logged in!', 'success')
            if user.is_seller():
                return redirect(url_for('sellers.dashboard'))
            else:
                 return redirect(url_for('main.index'))  
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')          
    return render_template('users/login.html',form=form)

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:  # type: ignore
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('users/reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated: # type: ignore
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)

    print("the user is------------",user)
    if user is None:
        print("the user is------------",user)
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password = form.password.data
        user.password = password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/reset_token.html', title='Reset Password', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@users.route("/account",methods=['GET','POST'])
@login_required
def account():
    form = AccountEditForm()
    if form.validate_on_submit():
        if form.profile_pic.data:
            picture_file = save_picture(form.profile_pic.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username  # type: ignore
        form.email.data = current_user.email  # type: ignore
        form.address.data = current_user.address  # type: ignore
        form.country.data = current_user.country  # type: ignore
        form.town.data = current_user.town  # type: ignore
    image_file = url_for('static', filename='uploads/user-profiles/' +
                         current_user.image_file)  # type: ignore
    return render_template('users/account.html', title='Account', image_file=image_file, form=form)



    

