from flask import render_template, redirect, url_for, flash, get_flashed_messages, request
from Fitnet import app, db
from Fitnet.form import RegisterForm, LoginForm, RoutineForm, EmptyForm
from Fitnet.model import Users, Post
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/home", methods=['GET', 'POST'])
@app.route("/home/feed", methods=['GET', 'POST'])
@login_required
def home():
    form = EmptyForm()
    username = form.username.data
    if form.validate_on_submit():
        user = Users.query.filter_by(user_name=username).first()
        if user is None:
            flash('User {} not found.'.format(username), category='danger')
            return redirect(url_for('home'))
        if user == current_user:
            flash('You cannot follow yourself!', category='info')
            return redirect(url_for('home'))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username), category='success')
        return redirect(url_for('home'))
    # else:
    #     return redirect(url_for('home'))
    #
    # return render_template('home.html', form=form)
    return render_template('home.html', user=current_user, form=form)

@app.route("/home/profile")
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    form = RegisterForm()
    if form.validate_on_submit():
        user = Users(user_name=form.username.data,
                     email_address=form.email_address.data,
                     password=generate_password_hash(form.password.data, method='sha256'))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('log_in'))

    if form.errors != {}:
        for err in form.errors.values():
            flash("%s" %(err[0]), category='danger')

    return render_template('sign_up1.html', form=form)

@app.route("/log_in", methods=['GET', 'POST'])
def log_in():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = Users.query.filter_by(email_address=form.email_address.data).first()
        if attempted_user and check_password_hash(attempted_user.password, form.password.data):
            login_user(attempted_user)
            # flash("Logged in!")
            return redirect(url_for('home'))
        else:
            flash("Incorrect email or password", category='danger')

    return render_template('log_in.html', form=form)

@app.route('/log_out')
def log_out():
    logout_user()
    return redirect(url_for('index'))

@app.route('/home/routines', methods=['GET', 'POST'])
def routines():
    form = RoutineForm()
    if request.method == 'POST':
        type = request.form.getlist('type')
        type = ', '.join([str(elem) for elem in type])
        routine = Post(name=request.form.get('name'),
                           duration=request.form.get('duration'),
                           type=type,
                           equipment=request.form.get('equipment'),
                           exercises=request.form.get('exercises'),
                           author_id=current_user.id
                           )

        db.session.add(routine)
        db.session.commit()
        return redirect(url_for('home'))

    if form.errors != {}:
        for err in form.errors.values():
            flash("%s" %(err[0]), category='danger')
    return render_template('routines.html', form=form)

@app.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    # p = Post.query.filter_by(id=1).first()
    # p.likes.count()
    return redirect(request.referrer)

@app.route('/profile/<username>')
@login_required
def user(username):
    user = Users.query.filter_by(user_name=username).first_or_404()
    return render_template('profile.html', user=user)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    post_to_delete = Post.query.get_or_404(id)

    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        return redirect(request.referrer)
    except:
        flash("Error", category='danger')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    post = Post.query.get_or_404(id)
    form = RoutineForm()
    if request.method == 'POST':
        type = request.form.getlist('type')
        type = ', '.join([str(elem) for elem in type])
        post.name = request.form.get('name')
        post.duration = request.form.get('duration')
        post.type = type
        post.equipment = request.form.get('equipment')
        post.exercises = request.form.get('exercises')

        try:
            db.session.commit()
            return redirect(url_for('home'))
        except:
            flash("Error", category='danger')
    else:
        return render_template('update_routines.html', form=form)

# @app.route('/unfollow/<username>', methods=['POST'])
# @login_required
# def unfollow(username):
#     form = EmptyForm()
#     if form.validate_on_submit():
#         user = Users.query.filter_by(username=username).first()
#         if user is None:
#             flash('User {} not found.'.format(username))
#             return redirect(url_for('index'))
#         if user == current_user:
#             flash('You cannot unfollow yourself!')
#             return redirect(url_for('user', username=username))
#         current_user.unfollow(user)
#         db.session.commit()
#         flash('You are not following {}.'.format(username))
#         return redirect(url_for('user', username=username))
#     else:
#         return redirect(url_for('index'))
