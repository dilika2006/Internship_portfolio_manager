from flask import Flask, render_template, redirect, url_for, request, session, flash
from database import db, User, Internship, Skill, Project, Certificate
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


# ---- Business Logic Functions ----

def is_valid_username(username):
    return len(username) >= 3

def is_valid_password(password):
    return len(password) >= 6

def internship_belongs_to_user(internship_user_id, session_user_id):
    return internship_user_id == session_user_id


# ---- Routes ----

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not is_valid_username(username):
            flash('Username must be at least 3 characters.')
            return redirect(url_for('register'))

        if not is_valid_password(password):
            flash('Password must be at least 6 characters.')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Choose another.')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created! Please login.')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login first.')
        return redirect(url_for('login'))
    internships = Internship.query.filter_by(user_id=session['user_id']).all()
    return render_template('dashboard.html', internships=internships)


@app.route('/add', methods=['GET', 'POST'])
def add_internship():
    if 'user_id' not in session:
        flash('Please login first.')
        return redirect(url_for('login'))
    if request.method == 'POST':
        new_internship = Internship(
            company=request.form['company'],
            role=request.form['role'],
            start_date=request.form['start_date'],
            end_date=request.form['end_date'],
            notes=request.form['notes'],
            skills=request.form['skills'],
            user_id=session['user_id']
        )
        db.session.add(new_internship)
        db.session.commit()
        flash('Internship added!')
        return redirect(url_for('dashboard'))
    return render_template('add.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_internship(id):
    if 'user_id' not in session:
        flash('Please login first.')
        return redirect(url_for('login'))
    internship = Internship.query.get_or_404(id)
    if not internship_belongs_to_user(internship.user_id, session['user_id']):
        flash('You cannot edit this internship.')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        internship.company = request.form['company']
        internship.role = request.form['role']
        internship.start_date = request.form['start_date']
        internship.end_date = request.form['end_date']
        internship.notes = request.form['notes']
        internship.skills = request.form['skills']
        db.session.commit()
        flash('Internship updated!')
        return redirect(url_for('dashboard'))
    return render_template('edit.html', internship=internship)


@app.route('/delete/<int:id>')
def delete_internship(id):
    if 'user_id' not in session:
        flash('Please login first.')
        return redirect(url_for('login'))
    internship = Internship.query.get_or_404(id)
    if not internship_belongs_to_user(internship.user_id, session['user_id']):
        flash('You cannot delete this internship.')
        return redirect(url_for('dashboard'))
    db.session.delete(internship)
    db.session.commit()
    flash('Internship deleted!')
    return redirect(url_for('dashboard'))


@app.route('/skills')
def skills():
    if 'user_id' not in session:
        flash('Please login first.')
        return redirect(url_for('login'))
    skills = Skill.query.filter_by(user_id=session['user_id']).all()
    return render_template('skills.html', skills=skills)


@app.route('/skills/add', methods=['GET', 'POST'])
def add_skill():
    if 'user_id' not in session:
        flash('Please login first.')
        return redirect(url_for('login'))
    if request.method == 'POST':
        new_skill = Skill(
            name=request.form['name'],
            level=request.form['level'],
            notes=request.form['notes'],
            user_id=session['user_id']
        )
        db.session.add(new_skill)
        db.session.commit()
        flash('Skill added!')
        return redirect(url_for('skills'))
    return render_template('add_skill.html')


@app.route('/skills/edit/<int:id>', methods=['GET', 'POST'])
def edit_skill(id):
    if 'user_id' not in session:
        flash('Please login first.')
        return redirect(url_for('login'))
    skill = Skill.query.get_or_404(id)
    if not internship_belongs_to_user(skill.user_id, session['user_id']):
        flash('You cannot edit this skill.')
        return redirect(url_for('skills'))
    if request.method == 'POST':
        skill.name = request.form['name']
        skill.level = request.form['level']
        skill.notes = request.form['notes']
        db.session.commit()
        flash('Skill updated!')
        return redirect(url_for('skills'))
    return render_template('edit_skill.html', skill=skill)


@app.route('/skills/delete/<int:id>')
def delete_skill(id):
    if 'user_id' not in session:
        flash('Please login first.')
        return redirect(url_for('login'))
    skill = Skill.query.get_or_404(id)
    if not internship_belongs_to_user(skill.user_id, session['user_id']):
        flash('You cannot delete this skill.')
        return redirect(url_for('skills'))
    db.session.delete(skill)
    db.session.commit()
    flash('Skill deleted!')
    return redirect(url_for('skills'))


@app.route('/projects')
def projects():
    if 'user_id' not in session:
        flash('Please login first.')
        return redirect(url_for('login'))
    projects = Project.query.filter_by(user_id=session['user_id']).all()
    return render_template('projects.html', projects=projects)


@app.route('/projects/add', methods=['GET', 'POST'])
def add_project():
    if 'user_id' not in session:
        flash('Please login first.')
        return redirect(url_for('login'))
    if request.method == 'POST':
        new_project = Project(
            title=request.form['title'],
            description=request.form['description'],
            start_date=request.form['start_date'],
            end_date=request.form['end_date'],
            link=request.form['link'],
            user_id=session['user_id']
        )
        db.session.add(new_project)
        db.session.commit()
        flash('Project added!')
        return redirect(url_for('projects'))
    return render_template('add_project.html')


@app.route('/projects/edit/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    if 'user_id' not in session:
        flash('Please login first.')
        return redirect(url_for('login'))
    project = Project.query.get_or_404(id)
    if not internship_belongs_to_user(project.user_id, session['user_id']):
        flash('You cannot edit this project.')
        return redirect(url_for('projects'))
    if request.method == 'POST':
        project.title = request.form['title']
        project.description = request.form['description']
        project.start_date = request.form['start_date']
        project.end_date = request.form['end_date']
        project.link = request.form['link']
        db.session.commit()
        flash('Project updated!')
        return redirect(url_for('projects'))
    return render_template('edit_project.html', project=project)


@app.route('/projects/delete/<int:id>')
def delete_project(id):
    if 'user_id' not in session:
        flash('Please login first.')
        return redirect(url_for('login'))
    project = Project.query.get_or_404(id)
    if not internship_belongs_to_user(project.user_id, session['user_id']):
        flash('You cannot delete this project.')
        return redirect(url_for('projects'))
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted!')
    return redirect(url_for('projects'))


@app.route('/certificates')
def certificates():
    if 'user_id' not in session:
        flash('Please login first.')
        return redirect(url_for('login'))
    certificates = Certificate.query.filter_by(user_id=session['user_id']).all()
    return render_template('certificates.html', certificates=certificates)


@app.route('/certificates/add', methods=['GET', 'POST'])
def add_certificate():
    if 'user_id' not in session:
        flash('Please login first.')
        return redirect(url_for('login'))
    if request.method == 'POST':
        new_certificate = Certificate(
            title=request.form['title'],
            issuer=request.form['issuer'],
            date_obtained=request.form['date_obtained'],
            link=request.form['link'],
            user_id=session['user_id']
        )
        db.session.add(new_certificate)
        db.session.commit()
        flash('Certificate added!')
        return redirect(url_for('certificates'))
    return render_template('add_certificate.html')


@app.route('/certificates/edit/<int:id>', methods=['GET', 'POST'])
def edit_certificate(id):
    if 'user_id' not in session:
        flash('Please login first.')
        return redirect(url_for('login'))
    certificate = Certificate.query.get_or_404(id)
    if not internship_belongs_to_user(certificate.user_id, session['user_id']):
        flash('You cannot edit this certificate.')
        return redirect(url_for('certificates'))
    if request.method == 'POST':
        certificate.title = request.form['title']
        certificate.issuer = request.form['issuer']
        certificate.date_obtained = request.form['date_obtained']
        certificate.link = request.form['link']
        db.session.commit()
        flash('Certificate updated!')
        return redirect(url_for('certificates'))
    return render_template('edit_certificate.html', certificate=certificate)


@app.route('/certificates/delete/<int:id>')
def delete_certificate(id):
    if 'user_id' not in session:
        flash('Please login first.')
        return redirect(url_for('login'))
    certificate = Certificate.query.get_or_404(id)
    if not internship_belongs_to_user(certificate.user_id, session['user_id']):
        flash('You cannot delete this certificate.')
        return redirect(url_for('certificates'))
    db.session.delete(certificate)
    db.session.commit()
    flash('Certificate deleted!')
    return redirect(url_for('certificates'))


if __name__ == '__main__':
    app.run(debug=True)