from mercuri.api import bp
from flask import request, jsonify, url_for, g, abort
from mercuri.models.user import User, db
from mercuri.api.errors import bad_request
from mercuri.api.auth import token_auth


@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    include_email = False
    # data = request.get_data() or {}
    # if 'include_email' in data and 'include_email' == True:
    #     include_email = True
    #     print(include_email)
    return jsonify(User.query.get_or_404(id).to_dict(include_email=include_email))


@bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    users = list()
    for user in User.query.all():
        users.append(user.to_dict(include_email=True))
    return jsonify(users)


@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}

    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    if g.current_user.id != id:
        # we're not even gonna waste on the rest lol
        abort(403)
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())
