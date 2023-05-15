from flask import Blueprint,render_template

main=Blueprint('main',__name__)


@main.route('/main')
def index():
    return render_template('main/index.html')