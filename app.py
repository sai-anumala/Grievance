from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change to a secure key in production

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grievances.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Grievance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    mood = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(50), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-grievance', methods=['POST'])
def submit_grievance():
    title = request.form.get('title')
    reason = request.form.get('reason')
    mood = request.form.get('mood')
    severity = request.form.get('severity')

    # Simple validation (optional)
    if not (title and reason and mood and severity):
        flash('Please fill in all fields.', 'danger')
        return redirect('/')

    grievance = Grievance(title=title, reason=reason, mood=mood, severity=severity)
    db.session.add(grievance)
    db.session.commit()

    flash('Grievance submitted successfully!', 'success')
    return redirect('/')
@app.route('/view-grievances')
def view_grievances():
    all_grievances = Grievance.query.all()
    return render_template('view_grievances.html', grievances=all_grievances)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)