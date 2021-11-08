from flask import Blueprint, json, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Language, Translation, User, Category, Tag, Post, Media, text_shorter
from sqlalchemy import desc
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
import uuid

main = Blueprint('main', __name__)

ROW_PER_PAGE = 10
ITEMS_LIMIT = 6

@main.route('/')
@login_required
def cpanel():  
    try:
        posts = Post.query.filter_by(published=True).order_by(desc(Post.lastUpdated)).limit(ITEMS_LIMIT).all()
        for i in posts:
            i.title = text_shorter(i.title, 45)

        categories = Category.query.order_by(desc(Category.id)).limit(ITEMS_LIMIT).all()
        for i in categories:
            i.category_name = text_shorter(i.category_name, 45)

        posts_cnt = db.session.execute('select count(id) from post').scalar()

        weekStart = datetime.now() - timedelta(weeks=1)
        posts_last_week = db.session.execute("select count(id) from post where " + 
                                            "lastUpdated > '" + str(weekStart) + "'").scalar()
        cats_cnt = db.session.execute('select count(id) from category').scalar()

        most_cat = db.session.execute('select b.category_name as name, count(category_id) as cnt from post as a '+
                                    'inner join category as b on a.category_id = b.id ' +
                                    'group by a.category_id order by count(a.category_id) desc, a.id limit 1')

        most_cat_row = None
        for row in most_cat:
            most_cat_row = row

        most_tag = db.session.execute('select b.tag_name as name, count (a.tag_id) as cnt from post_tag as a ' +
                                    'inner join tag as b on a.tag_id = b.id ' +
                                    'group by a.tag_id order by count(a.tag_id) desc, a.id limit 1')

        most_tag_row = None
        for row in most_tag:
            most_tag_row = row

        return render_template('cpanel.html', posts=posts, categories=categories, posts_cnt=posts_cnt, cats_cnt=cats_cnt, 
                            posts_last_week=posts_last_week, most_cat_row=most_cat_row, most_tag_row=most_tag_row)
    except Exception as ex:
        print('*** ' + str(datetime.now()) + ' *** cpanel msg: ' + str(ex))
        return redirect(url_for('errors.unknownerror'))

@main.route('/profile')
@login_required
def profile():
    posts_cnt = db.session.execute('select count(id) from post where owner_id=' + str(current_user.id)).scalar()

    return render_template('profile.html', name=current_user.name, posts_cnt=posts_cnt)

@main.route('/users')
@login_required
def users():
    try:
        search_txt = request.args.get('f')
        page = request.args.get('page', 1, type=int)
        if search_txt:
            users = User.query.filter(User.name.contains(search_txt)).paginate(page=page, per_page=ROW_PER_PAGE)    
        else:
            users = User.query.paginate(page=page, per_page=ROW_PER_PAGE)

        return render_template('users.html', collection=users, search_txt=search_txt)
    except Exception as ex:
        print('*** ' + str(datetime.now()) + ' *** users msg: ' + str(ex))
        return redirect(url_for('errors.unknownerror'))

@main.route('/categories')
@login_required
def categories():
    try:
        search_txt = request.args.get('f')
        page = request.args.get('page', 1, type=int)
        if search_txt:
            categories = Category.query.filter(Category.category_name.contains(search_txt)).paginate(page=page, per_page=ROW_PER_PAGE)
        else:
            categories = Category.query.paginate(page=page, per_page=ROW_PER_PAGE)

        langs = Language.query.all()
        data = {
            "langs": 
                [e.serialize() for e in langs]
        }
        return render_template('categories.html', collection=categories, search_txt=search_txt, langs=langs, langs_js=json.dumps(data))
    except Exception as ex:
        print('*** ' + str(datetime.now()) + ' *** categories msg: ' + str(ex))
        return redirect(url_for('errors.unknownerror'))

@main.route('/tags')
@login_required
def tags():
    try:
        search_txt = request.args.get('f')
        page = request.args.get('page', 1, type=int)
        if search_txt:
            tags = Tag.query.filter(Tag.tag_name.contains(search_txt)).paginate(page=page, per_page=ROW_PER_PAGE)    
        else:
            tags = Tag.query.paginate(page=page, per_page=ROW_PER_PAGE)

        return render_template('tags.html', collection=tags, search_txt=search_txt)
    except Exception as ex:
        print('*** ' + str(datetime.now()) + ' *** tags msg: ' + str(ex))
        return redirect(url_for('errors.unknownerror'))

@main.route('/posts')
@login_required
def posts():
    try:
        search_txt = request.args.get('f')
        page = request.args.get('page', 1, type=int)
        if search_txt:
            posts = Post.query.filter(Post.title.contains(search_txt)).paginate(page=page, per_page=ROW_PER_PAGE)
        else:
            posts = Post.query.paginate(page=page, per_page=ROW_PER_PAGE)

        return render_template('posts.html', collection = posts, search_txt=search_txt)
    except Exception as ex:
        print('*** ' + str(datetime.now()) + ' *** posts msg: ' + str(ex))
        return redirect(url_for('errors.unknownerror'))

@main.route('/images')
@login_required
def images():
    try:
        page = request.args.get('page', 1, type=int)
        imgs = Media.query.paginate(page=page, per_page=ROW_PER_PAGE)

        return render_template('images.html', collection=imgs)
    except Exception as ex:
        print('*** ' + str(datetime.now()) + ' *** images msg: ' + str(ex))
        return redirect(url_for('errors.unknownerror'))

@main.route('/init')
def init():
    user = User.query.filter_by(id=1).first()
    if user:
        return redirect(url_for('errors.unknownerror'))
    
    return render_template('init.html')

@main.route('/init', methods=['POST'])
def init_post():
    user = User.query.filter_by(id=1).first()
    if user:
        return redirect(url_for('errors.unknownerror'))

    try:
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        suser = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
        db.session.add(suser)
        db.session.commit()

        defaultCat = Category(category_name='Uncategorized', translation_id=str(uuid.uuid4()))
        db.session.add(defaultCat)
        db.session.commit()
    except Exception as ex:
        print('*** ' + str(datetime.now()) + ' *** init msg: ' + str(ex))
        return redirect(url_for('errors.unknownerror'))

    return redirect(url_for('auth.login'))

@main.route('/get_translation')
@login_required
def get_translation():
    try:
        lang = request.args.get('lang')
        id = request.args.get('id')
        trans = Translation.query.filter_by(lang=lang, translation_id=id).first()
        if not trans:
            return json.jsonify("")        
        return json.jsonify(trans.text)
    except Exception as ex:
        print('*** ' + str(datetime.now()) + ' *** get_translation msg: ' + str(ex))
        return json.jsonify("") 