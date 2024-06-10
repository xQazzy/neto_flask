from flask import Blueprint, request, jsonify, abort
from models import db, Ad, User
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

auth = HTTPBasicAuth()
bp = Blueprint('routes', __name__)

@auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None

@bp.route('/')
def home():
    return "Главная? ОНО ЖИВО!"

@bp.route('/ad', methods=['POST'])
@auth.login_required
def create_ad():
    data = request.get_json()
    new_ad = Ad(title=data['title'], description=data['description'], owner_id=auth.current_user().id)
    db.session.add(new_ad)
    db.session.commit()
    return jsonify({"message": "Объявление успешно добавлено!"}), 201

@bp.route('/ad/<int:ad_id>', methods=['GET'])
def get_ad(ad_id):
    ad = Ad.query.get_or_404(ad_id)
    return jsonify({
        'id': ad.id,
        'title': ad.title,
        'description': ad.description,
        'created_at': ad.created_at,
        'owner': ad.owner.email
    })

@bp.route('/ad/<int:ad_id>', methods=['DELETE'])
@auth.login_required
def delete_ad(ad_id):
    ad = Ad.query.get_or_404(ad_id)
    if ad.owner_id != auth.current_user().id:
        abort(403)
    db.session.delete(ad)
    db.session.commit()
    return jsonify({"message": "Сообщение успешно удалено!"})

@bp.route('/ad/<int:ad_id>', methods=['PUT'])
@auth.login_required
def update_ad(ad_id):
    ad = Ad.query.get_or_404(ad_id)
    if ad.owner_id != auth.current_user().id:
        abort(403)
    data = request.get_json()
    ad.title = data['title']
    ad.description = data['description']
    db.session.commit()
    return jsonify({"message": "Объявление успешно обновлено!"})

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    password = data['password']
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"message": "Пользователь с таким email уже зарегистрирован"}), 400
    new_user = User(email=email, password_hash=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Пользователь успешно создан!"}), 201