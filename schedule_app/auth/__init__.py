from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Невірний логін або пароль')
    
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        group = request.form.get('group')
        
        if User.query.filter_by(username=username).first():
            flash('Користувач з таким іменем вже існує')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Користувач з такою електронною поштою вже існує')
            return redirect(url_for('auth.register'))
        
        new_user = User(
            username=username,
            password=generate_password_hash(password),
            email=email,
            group=group,
            is_admin=False
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Реєстрація успішна! Тепер ви можете увійти.')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index')) 