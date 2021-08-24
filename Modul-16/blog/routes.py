from flask import render_template, request, flash, url_for, redirect, session
from blog import app
from blog.models import Entry, db
from blog.forms import LoginForm
from blog.utils import generate_fake_posts, delete_posts, get_entries
import functools


def login_required(view_func):
    @functools.wraps(view_func)
    def check_permissions(*args, **kwargs):
        if session.get('logged_in'):
            return view_func(*args, **kwargs)
        return redirect(url_for('login', next=request.path))
    return check_permissions


@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    errors = None
    next_url = request.args.get('next')
    if request.method == 'POST':
        if form.validate_on_submit():
            session['logged_in'] = True
            session.permanent = True
            flash('You are now logged in.', 'success')
            return redirect(next_url or url_for('index'))
        else:
            errors = form.errors
    return render_template("login_form.html", form=form, errors=errors)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        flash('You are now logged out.', 'success')
    return redirect(url_for('index'))


@app.route("/")
def index():
    all_posts = Entry.query.filter_by(
        is_published=True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_posts=all_posts)


@app.route("/drafts/", methods=['GET'])
@login_required
def list_drafts():
    drafts = Entry.query.filter_by(
        is_published=False).order_by(Entry.pub_date.desc())
    return render_template("drafts.html", drafts=drafts)


@app.route("/gen/")
@login_required
def generate_posts():
    delete_posts()
    all_posts = generate_fake_posts(how_many=10)
    flash(f'Old posts were deleted and 10 new random ones were generated.')
    return render_template("homepage.html", all_posts=all_posts)


@app.route("/delete_post/<int:entry_id>", methods=['POST'])
@login_required
def delete_entry(entry_id):
    if request.method == 'POST':
        entry = Entry.query.filter_by(id=entry_id).first_or_404()
        db.session.delete(entry)
        db.session.commit()
        flash(f'Post deleted {entry.title} on the blog.')
    return redirect(url_for('index'))


@app.route("/new-post/", methods=["GET", "POST"])
@login_required
def create_entry():
    return get_entries(entry_id=0)


@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
@login_required
def edit_entry(entry_id):
    return get_entries(entry_id)
