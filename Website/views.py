from flask import Blueprint, render_template

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('SignPage.html')

@views.route('/survey')
def survey():
    return render_template('survey.html')

@views.route('/about')
def about():
    return render_template('about us.html')

@views.route('/symptoms')
def symptoms():
    return render_template('covid symptoms.html')
