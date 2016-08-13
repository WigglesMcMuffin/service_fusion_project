from flask import Blueprint, render_template, redirect, url_for, request
from flask_app.forms import UserForm

main_site = Blueprint('main', __name__, template_folder='templates', static_folder='static')

@main_site.route('/')
def main_page():
    user_form = UserForm()
    update_form = UserForm()
    return render_template('main.jade', userform=user_form, updateform=update_form, pageTitle='Home Page')

@main_site.route('/service_fusion/')
def test_page():
    user_form = UserForm()
    update_form = UserForm()
    return render_template('main.jade', userform=user_form, updateform=update_form, pageTitle='Test Page')
