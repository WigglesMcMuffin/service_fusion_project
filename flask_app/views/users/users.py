from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask.views import MethodView
from flask_app.models.base import db, User, UserSchema
from flask_app.forms import UserForm

user_site = Blueprint('user', __name__, template_folder='templates', url_prefix='/user', static_folder='static')

class UserAPI(MethodView):
  def get(self, user_id=None):
    if user_id is None:
      #get all users
      user_query = None
      if int(request.args.get('page', 0)) > 0:
        user_query = User.query.order_by(User.last_name).paginate(int(request.args.get('page')), 30, False)
      else:
        user_query = User.query.paginate(1, 30, False)
      total = user_query.total
      users = user_query.items
      message = {
        'status': '200',
        'message': UserSchema().dump(users, many=True).data,
        'next_page': user_query.has_next
      }
      resp = jsonify(message)
      resp.status_code = 200
      return resp
    else:
      #Get specific user
      user = User.query.get(user_id)
      if user:
        message = {
          'user': UserSchema().dump(user).data,
          'status': 200
        }
        resp = jsonify(message)
        resp.status_code = 200
        return resp
      else:
        message = {
          'status': 404,
          'message': 'No user found with id: %s' %(user_id)
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp

  def post(self):
    #Create new users
    form = UserForm()
    if form.validate_on_submit():
      user = User()
      form.populate_obj(user)
      first_name = form.first_name.data.strip()
      last_name = form.last_name.data.strip()
      date_of_birth = form.date_of_birth.data
      zip_code = form.zip_code.data.strip()
      db.session.add(user)
      db.session.flush()
      user_id = user.id
      db.session.commit()
      message = {
        'message': 'User added',
        'first_name': first_name,
        'last_name': last_name,
        'id': user_id,
        'status': 200
      }
      resp = jsonify(message)
      resp.status_code = 200
      return resp
    else:
      message = {
        'status': 400,
        'message': 'User creation failed',
        'errors': form.errors
      }
      resp = jsonify(message)
      resp.status_code = 400
      return resp

  def delete(self, user_id=None):
    if user_id is None:
      #Raise error, user_id required
      message = {
        'status': 400,
        'message': 'User id required to DELETE'
      }
      resp = jsonify(message)
      resp.status_code = 400
      return resp
    else:
      #Delete User
      user = User.query.get(user_id)
      if user:
        db.session.delete(user)
        db.session.commit()
        message = {
          'message': 'User: %s, %s removed' %(user.last_name, user.first_name),
          'status': 200
        }
        resp = jsonify(message)
        resp.status_code = 200
        return resp
      else:
        message = {
          'status': 404,
          'message': 'No user found with id: %s' %(user_id)
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp

  def put(self, user_id=None):
    if user_id is None:
      #Riase error, user_id required
      message = {
        'status': 400,
        'message': 'User id required to update'
      }
      resp = jsonify(message)
      resp.status_code = 400
      return resp
    else:
      #Update single user
      user = User.query.get(user_id)
      if user:
        form = UserForm()
        if form.validate_on_submit():
          user.first_name = form.first_name.data
          user.last_name = form.last_name.data
          user.date_of_birth = form.date_of_birth.data
          user.zip_code = form.zip_code.data
          db.session.commit()
          message = {
            'message': 'User: %s, %s updated' %(user.last_name, user.first_name),
            'user': UserSchema().dump(user).data,
            'status': 200
          }
          resp = jsonify(message)
          resp.status_code = 200
          return resp
        else:
          message = {
            'status': 400,
            'message': 'Form Fields Not Validated Correctly',
            'errors': form.errors
          }
          resp = jsonify(message)
          resp.status_code = 400
          return resp
      else:
        message = {
          'status': 404,
          'message': 'No user found with id: %s' %(user_id)
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp

user_view = UserAPI.as_view('user_api')
user_site.add_url_rule('/', defaults={'user_id': None},
                       view_func=user_view, methods=['GET'])
user_site.add_url_rule('/', view_func=user_view, methods=['POST'])
user_site.add_url_rule('/<user_id>', view_func=user_view,
                       methods=['GET', 'PUT', 'DELETE'])
