from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_required, current_user
from datetime import datetime
import os

from models import db, User, Schedule

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schedule.db'

# Initialize extensions
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import and register blueprints
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schedule')
def view_schedule():
    group = request.args.get('group')
    date = request.args.get('date')
    teacher_id = request.args.get('teacher_id')
    
    query = Schedule.query
    
    if group:
        query = query.filter_by(group=group)
    if date:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        query = query.filter(db.func.date(Schedule.date) == date_obj.date())
    if teacher_id:
        query = query.filter_by(teacher_id=teacher_id)
    
    schedules = query.order_by(Schedule.date, Schedule.start_time).all()
    teachers = User.query.filter_by(is_admin=True).all()
    return render_template('schedule.html', schedules=schedules, teachers=teachers)

@app.route('/admin/schedule', methods=['GET', 'POST'])
@login_required
def manage_schedule():
    if not current_user.is_admin:
        flash('Доступ заборонено')
        return redirect(url_for('index'))
    
    edit_id = request.args.get('edit_id')
    schedule = Schedule.query.get(edit_id) if edit_id else None
    
    if request.method == 'POST':
        schedule_id = request.form.get('schedule_id')
        
        if schedule_id:
            schedule = Schedule.query.get(schedule_id)
            if schedule:
                schedule.subject = request.form['subject']
                schedule.group = request.form['group']
                schedule.date = datetime.strptime(request.form['date'], '%Y-%m-%d')
                schedule.start_time = request.form['start_time']
                schedule.end_time = request.form['end_time']
                schedule.room = request.form['room']
                flash('Заняття оновлено')
        else:
            new_schedule = Schedule(
                subject=request.form['subject'],
                teacher_id=current_user.id,
                group=request.form['group'],
                date=datetime.strptime(request.form['date'], '%Y-%m-%d'),
                start_time=request.form['start_time'],
                end_time=request.form['end_time'],
                room=request.form['room']
            )
            db.session.add(new_schedule)
            flash('Заняття додано')
        
        db.session.commit()
        return redirect(url_for('manage_schedule'))
    
    schedules = Schedule.query.filter_by(teacher_id=current_user.id).order_by(Schedule.date).all()
    return render_template('admin/schedule.html', schedules=schedules, schedule=schedule)

@app.route('/admin/schedule/<int:schedule_id>/delete', methods=['POST'])
@login_required
def delete_schedule(schedule_id):
    if not current_user.is_admin:
        flash('Доступ заборонено')
        return redirect(url_for('index'))
    
    schedule = Schedule.query.get_or_404(schedule_id)
    if schedule.teacher_id != current_user.id:
        flash('Ви не можете видалити це заняття')
        return redirect(url_for('manage_schedule'))
    
    db.session.delete(schedule)
    db.session.commit()
    flash('Заняття видалено')
    return redirect(url_for('manage_schedule'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 