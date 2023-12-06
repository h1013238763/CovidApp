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

@views.route('/FAQ')
def faq():
    return render_template('Faq page.html')

@views.route('/blog')
def blog():
    return render_template('blog.html')

@views.route('/userhome')
def userhome():
    return render_template('index.html')

