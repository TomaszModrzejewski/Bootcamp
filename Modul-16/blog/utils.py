from flask import render_template, request, flash, url_for, redirect, session
from blog.models import Entry, db
from blog.forms import EntryForm
from faker import Faker


def generate_fake_posts(how_many=10):
    fake = Faker()

    for _ in range(how_many):
        post = Entry(
            title=fake.sentence(),
            body='\n'.join(fake.paragraphs(15)),
            is_published=True
        )
        db.session.add(post)
    db.session.commit()
    all_posts = Entry.query.all()
    return all_posts


def delete_posts():
    all_posts = Entry.query.all()
    for post in all_posts:
        db.session.delete(post)
    db.session.commit()


def get_entries(entry_id):
    errors = None
    if entry_id != 0:
        entry = Entry.query.filter_by(id=entry_id).first_or_404()
        form = EntryForm(obj=entry)
        flash_mess = f'edited post {entry.title} on the blog.'

    else:
        form = EntryForm()
        entry = Entry(
            title=form.title.data,
            body=form.body.data,
            is_published=form.is_published.data
        )
        flash_mess = f'Post added {entry.title} on the blog.'

    if request.method == 'POST':
        if form.validate_on_submit():
            if entry_id != 0:
                form.populate_obj(entry)
            else:
                db.session.add(entry)
            db.session.commit()
            flash(flash_mess)
            return redirect(url_for("index"))
        else:
            errors = form.errors

    return render_template("entry_form.html", form=form, errors=errors)
