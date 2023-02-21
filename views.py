# storing standard roots for website (home page, things user can navigate to)
from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Note
from . import db
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if (len(note) < 1):
            flash('note too short', category="error")
        else:
            newNote = Note(data=note, user_id=current_user.id)
            db.session.add(newNote)
            db.session.commit()
            flash("note is added", category="success")
    return render_template("home.html", user=current_user)
