from flask import Blueprint, render_template, redirect, request, url_for, flash, Markup
from flask_login import login_required, current_user
from . import db, csrf
from .models import User, Post, Category, Tag, PostTag
from datetime import datetime
from bs4 import BeautifulSoup
from .img import save_img
import bleach

posts = Blueprint('posts', __name__)

ALLOWED_TAGS = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'span', 'br', 'img', 'pre', 'b', 'div', 'u', 'a', 'i', 'font']
ALLOWED_ATTRS = {'*': ['style', 'src', 'class', 'target', 'href', 'align']}
ALLOWED_STYLES = ['color', 'text-align', 'font-weigth', 'font-family', 'font-size', 'align']

# Post
@posts.route('/newpost')
@login_required
def new_post():
    cat_id = request.args.get('cat', 1, type=int)
    post = Post(title='', full='', publishDate=datetime.now(), lastUpdated=datetime.now(),
                    category_id=1, published=False, imgMain='default.jpg', shortDesc='', id=0, owner_id=current_user.id)
    tagsString = ''
    return render_template('post.html', categories=Category.query.all(), tags=Tag.query.all(), post=post, tagsString=tagsString,
    owner_name=current_user.name, category=cat_id, dateAdd=post.publishDate.strftime("%Y-%m-%d %H:%M"),
    dateUpdate=post.lastUpdated.strftime("%Y-%m-%d %H:%M"))

@posts.route('/editpost/<id>')
@login_required
def edit_post(id):
    try:
        post = Post.query.filter_by(id=id).first()
        tags = db.session.execute('select a.id, a.tag_name from tag as a ' +
                                'inner join post_tag as b on a.id = b.tag_id where b.post_id = ' + str(id))
        tagsString = ''
        for i in tags:
            tagsString += i.tag_name + ', '
        tagsString = tagsString[:-2]

        user = User.query.filter_by(id=post.owner_id).first()
        return render_template('post.html', categories=Category.query.all(), tags=Tag.query.all(), post=post, tagsString=tagsString,
        owner_name=user.name, dateAdd=post.publishDate.strftime("%Y-%m-%d %H:%M"),
        dateUpdate=post.lastUpdated.strftime("%Y-%m-%d %H:%M"))
    except Exception as ex:
        print('*** ' + str(datetime.now()) + ' *** edit_post msg: ' + str(ex))
        return redirect(url_for('errors.unknownerror'))

@posts.route('/dpost/<id>', methods=['GET','POST'])
@login_required
def dpost(id):
    try:
        post = Post.query.filter_by(id=id).first()
        postname = post.title
        dposttags = PostTag.__table__.delete().where(PostTag.post_id == id)
        db.session.delete(post)
        db.session.execute(dposttags)
        db.session.commit()
        flash(Markup('Post <strong>' + postname + '</strong> was deleted!'))
        flash('success')
        return redirect(url_for('main.posts'))
    except Exception as ex:
        print('*** ' + str(datetime.now()) + ' *** dpost msg: ' + str(ex))
        return redirect(url_for('errors.unknownerror'))

@posts.route('/savepost/<id>', methods=['POST'])
@login_required
def save_post(id):
    try:
        title = request.form.get('title')
        full = request.form.get('editordata')
        publish = request.form.get('publish_select')
        category = request.form.get('category_select')
        shortDesc = request.form.get('short_desc')
        storageImage = request.form.get('storage_img')
        tags = request.form.get('tags').replace(' ,', ',').replace(', ',',')

        full = bleach.clean(full, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, styles=ALLOWED_STYLES)

        finalTags = create_final_tags(tags)

        if not shortDesc:
            soup = BeautifulSoup(full, 'html.parser')
            para = soup.find('p')
            if para:
                shortDesc = para.get_text()
            
        if len(shortDesc) > 300:
            shortDesc = shortDesc.partition('.')[0] + '.'

        published = False
        if publish == 'publish':
            published = True

        npost = Post(title=title, full=full, publishDate=datetime.now(), lastUpdated=datetime.now(),
            category_id=category, published=published, imgMain='', shortDesc=shortDesc, owner_id=current_user.id)
        imgName = storageImage
        if imgName == '':
            imgName = save_img(request.files)
        
        if int(id) == 0:        
            if imgName == '':
                imgName = 'default.jpg'
            npost.imgMain = imgName
            db.session.add(npost)
            db.session.commit()

            for i in finalTags:
                postTag = PostTag(post_id=npost.id, tag_id=i.id)
                db.session.add(postTag)
                db.session.commit()
            flash('Post created!')
            flash('success')
            return redirect(url_for('posts.edit_post', id=npost.id))    

        opost = Post.query.filter_by(id=id).first()

        npost.imgMain = opost.imgMain
        if imgName != '' and imgName != opost.imgMain:
            npost.imgMain = imgName

        update_post(opost, npost, finalTags)
        flash('Saved!')
        flash('success')
        return redirect(url_for('posts.edit_post', id=opost.id))
    except Exception as ex:
        print('*** ' + str(datetime.now()) + ' *** save_post msg: ' + str(ex))
        return redirect(url_for('errors.unknownerror'))

# End Post

# Categories
@posts.route('/addcategory', methods=['POST'])
@login_required
def categories_post():
    try:
        cat_name = request.form.get('category_name')
        duplicate_cats = Category.query.filter_by(category_name=cat_name).all()
        if duplicate_cats:
            flash(Markup('Category <strong>' + str(cat_name) + '</strong> already exist!'))
            flash('danger')
            return redirect(url_for('main.categories'))

        cat = Category.query.filter_by(category_name=cat_name).first()
        if cat:
            flash('Category already exists.')
            return redirect(url_for('main.categories'))

        new_cat = Category(category_name=cat_name)

        db.session.add(new_cat)
        db.session.commit()

        flash(Markup('Category <strong>' + cat_name + '</strong> was succussfully added!'))
        flash('success')
        return redirect(url_for('main.categories')) 
    except Exception as ex:
        print('*** ' + str(datetime.now()) + ' *** categories_post msg: ' + str(ex))
        return redirect(url_for('errors.unknownerror'))

@posts.route('/dcat/<id>', methods=['GET', 'POST'])
@login_required
def dcat(id):
    try:
        cat = Category.query.filter_by(id=id).first()
        name = cat.category_name
        posts = Post.query.filter_by(category_id=id).all()
        for i in posts:
            i.category_id = 1

        db.session.delete(cat)
        db.session.commit()
        flash(Markup('Category <strong>' + str(name) + '</strong> was deleted! All posts that were in this category '+
        'have been moved to <strong>uncategorized</strong>'))
        flash('success')
        return redirect(url_for('main.categories'))
    except Exception as ex:
        print('*** ' + str(datetime.now()) + ' *** dcat msg: ' + str(ex))
        return redirect(url_for('errors.unknownerror'))

@posts.route('/ucat/<id>', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def ucat(id):
    try:
        new_name = request.form.get('category_name')
        duplicate_cats = Category.query.filter_by(category_name=new_name).all()
        if duplicate_cats:
            flash(Markup('Category <strong>' + str(new_name) + '</strong> already exist!'))
            flash('danger')
            return redirect(url_for('main.categories'))

        cat = Category.query.filter_by(id=id).first()
        old_name = cat.category_name
        cat.category_name = new_name
        db.session.commit()
        flash(Markup('Category <strong>' + str(old_name) + '</strong> was renamed to '+
                    '<strong>' + new_name +'</strong>!'))
        flash('success')
        return redirect(url_for('main.categories'))
    except Exception as ex:
        print('*** ' + str(datetime.now()) + ' *** ucat msg: ' + str(ex))
        return redirect(url_for('errors.unknownerror'))

# End Categories

# Tags
@posts.route('/dtag/<id>', methods=['GET', 'POST'])
@login_required
def dtag(id):
    try:
        tag = Tag.query.filter_by(id=id).first()
        name = tag.tag_name

        tagposts = PostTag.query.filter_by(tag_id=tag.id).all()
        for i in tagposts:
            db.session.delete(i)

        db.session.delete(tag)
        db.session.commit()
        flash(Markup('Tag <strong>' + str(name) + '</strong> was deleted! '+
        'This tag has been removed from all posts that used it.'))
        flash('success')
 
        return redirect(url_for('main.tags'))
    except Exception as ex:
        print('*** ' + str(datetime.now()) + ' *** dtag msg: ' + str(ex))
        return redirect(url_for('errors.unknownerror'))

@posts.route('/utag/<id>', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def utag(id):
    try:
        new_name = request.form.get('tag_name')
        tag = Tag.query.filter_by(id=id).first()
        old_name = tag.tag_name
        tag.tag_name = new_name
        db.session.commit()
        flash(Markup('Tag <strong>' + str(old_name) + '</strong> was renamed to '+
                    '<strong>' + new_name +'</strong>!'))
        flash('success')
        return redirect(url_for('main.tags'))
    except Exception as ex:
        print('*** ' + str(datetime.now()) + ' *** utag msg: ' + str(ex))
        return redirect(url_for('errors.unknownerror'))

# End Tags

# Defs

def create_final_tags(tags):
    tagsList = tags.split(',')
    finalTags = []

    for i in tagsList:
        checkExist = Tag.query.filter_by(tag_name=i).first()

        if checkExist:
            finalTags.append(checkExist)
        else:
            if i != '':
                tag = Tag(tag_name=i.lower())
                db.session.add(tag)
                db.session.commit()
                finalTags.append(tag)
    return finalTags

def update_post(opost, npost, tags):
    posttags = PostTag.query.filter_by(post_id=opost.id).all()
    for i in tags:
        if not any(x.tag_id == i.id for x in posttags):
            posttag = PostTag(post_id=opost.id, tag_id=i.id)
            db.session.add(posttag)
            db.session.commit()

    for i in posttags:
        if not any(x.id == i.tag_id for x in tags):
            db.session.delete(i)
            db.session.commit()

    opost.lastUpdated = datetime.now()
    if opost.title != npost.title:
        opost.title = npost.title
    if opost.full != npost.full:
        opost.full = npost.full
    if opost.shortDesc != npost.shortDesc:
        opost.shortDesc = npost.shortDesc
    if opost.category_id != npost.category_id:
        opost.category_id = npost.category_id
    if opost.imgMain != npost.imgMain:
        opost.imgMain = npost.imgMain
    if opost.published != npost.published:
        opost.published = npost.published
    
    db.session.commit()

# End Defs