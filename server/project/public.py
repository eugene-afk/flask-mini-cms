from flask import Blueprint, jsonify, request
from .models import Language, Post, Tag, PostTag, Category

public = Blueprint('public', __name__)

ROW_PER_PAGE = 10

@public.route('/api/posts', methods=['GET'])
def get_all_posts():
    try:
        lang = request.args.get('lang', "", type=str)
        lang_data = Language.query.filter_by(lang_code=lang).first()
        if not lang_data:
            lang = ""
        page = request.args.get('page', 1, type=int)
        row_per_page = request.args.get('rowsperpage', ROW_PER_PAGE, type=int)

        posts = Post.query.filter_by(published=True).paginate(page=page, per_page=row_per_page)
        data = {
            'total_pages': posts.pages,
            'current_page': posts.page,
            'posts': 
                [e.serialize_short(lang) for e in posts.items]
        }
    except Exception as ex:
        data = {
            'error': str(ex)
        }
    return jsonify(data)

@public.route('/api/posts/<int:id>', methods=['GET'])
def get_posts_by_category_id(id):
    try:
        lang = request.args.get('lang', "", type=str)
        lang_data = Language.query.filter_by(lang_code=lang).first()
        if not lang_data:
            lang = ""
        tag_ids = request.args.getlist('tag')
        page = request.args.get('page', 1, type=int)
        row_per_page = request.args.get('rowsperpage', ROW_PER_PAGE, type=int)

        if tag_ids:
            sql_tags_filter = []
            for i in tag_ids:
                sql_tags_filter.append(i)
                
            posts = Post.query.filter_by(published=True, category_id=id).join(PostTag,
            Post.id == PostTag.post_id).filter(PostTag.tag_id.in_(sql_tags_filter)).paginate(page=page, per_page=row_per_page)
        else:
            posts = Post.query.filter_by(published=True, category_id=id).paginate(page=page, per_page=row_per_page)

        data = { 
            'total_pages': posts.pages,
            'current_page': posts.page,
            'posts': 
                [e.serialize_short(lang) for e in posts.items]
        }
    except Exception as ex:
        data = {
            'error': str(ex)
        }
    return jsonify(data)

@public.route('/api/post/<id>', methods=['GET'])
def get_post_by_id(id):
    try:
        lang = request.args.get('lang', "", type=str)
        lang_data = Language.query.filter_by(lang_code=lang).first()
        if not lang_data:
            lang = ""
        post = Post.query.filter_by(id=id, published=True).first()
        return jsonify(post.serialize(lang))
    except Exception as ex:
        data = {
            'error': str(ex)
        }
        return jsonify(data)

@public.route('/api/tags/<int:id>', methods=['GET'])
def get_tags_by_post_id(id):
    try:
        post_tags = PostTag.query.filter_by(post_id=id).all()
        tags = []
        for i in post_tags:
            tag = Tag.query.filter_by(id=i.tag_id).first()
            tags.append(tag)
        data = {
            'tags':
                [e.serialize() for e in tags]
        }
    except Exception as ex:
        data = {
            'error': str(ex)
        }
    return jsonify(data)

@public.route('/api/tags/bycategory/<int:id>', methods=['GET'])
def get_tags_by_category_id(id):
    try:
        tags = Tag.query.join(PostTag, Tag.id == PostTag.tag_id).join(Post,
        PostTag.post_id == Post.id).join(Category, Post.category_id == Category.id).filter_by(id=id)
        data = {
            'tags':
                [e.serialize() for e in tags]
        }
    except Exception as ex:
        data = {
            'error': str(ex)
        }
    return jsonify(data)

@public.route('/api/categories', methods=['GET'])
def get_categories():
    try:
        lang = request.args.get('lang', "", type=str)
        lang_data = Language.query.filter_by(lang_code=lang).first()
        if not lang_data:
            lang = ""
        cats = Category.query.all()
        data = {
            'categories':
                [e.serialize(lang) for e in cats]
        }
        
    except Exception as ex:
        data = {
            'error': str(ex)
        }
    return jsonify(data)
