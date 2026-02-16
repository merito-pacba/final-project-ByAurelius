import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Database Configuration (Using Environment Variables for Azure)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///travel.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class Travel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

# Create Database
with app.app_context():
    db.create_all()

# ROUTES
@app.route('/')
def index():
    travels = Travel.query.order_by(Travel.date_posted.desc()).all()
    return render_template('index.html', travels=travels)

@app.route('/add', methods=['GET', 'POST'])
def add_travel():
    if request.method == 'POST':
        city = request.form.get('city')
        description = request.form.get('description')
        new_entry = Travel(city=city, description=description)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_travel(id):
    entry = Travel.query.get_or_404(id)
    if request.method == 'POST':
        entry.city = request.form.get('city')
        entry.description = request.form.get('description')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', travel=entry)

@app.route('/delete/<int:id>')
def delete_travel(id):
    entry = Travel.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)