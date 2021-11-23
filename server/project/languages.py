from flask import Blueprint, render_template, request, redirect, url_for, flash, Markup
from flask_login import login_required
from . import db, csrf, logger
from .models import Language, Translation
from datetime import datetime

languages = Blueprint('languages', __name__)

ROW_PER_PAGE = 10
ITEMS_LIMIT = 6

@languages.route('/languages')
@login_required
def langs():
    try:
        search_txt = request.args.get('f')
        page = request.args.get('page', 1, type=int)
        if search_txt:
            langs = Language.query.filter(Language.lang_name.contains(search_txt)).paginate(page=page, per_page=ROW_PER_PAGE)
        else:
            langs = Language.query.paginate(page=page, per_page=ROW_PER_PAGE)

        return render_template('languages.html', collection=langs, search_txt=search_txt)
    except Exception as ex:
        print('*** ' + str(datetime.now()) + ' *** langs msg: ' + str(ex))
        logger.error(f"langs msg: {ex}")
        return redirect(url_for('errors.unknownerror'))

@languages.route('/addlanguage', methods=['POST'])
@login_required
def language_post():
    try:
        lang_name = request.form.get('language_name')
        lang_code = request.form.get('language_code')
        duplicate_langs = Language.query.filter_by(lang_name=lang_name).all()
        duplicate_codes = Language.query.filter_by(lang_code=lang_code).all()
        if duplicate_langs or duplicate_codes:
            flash(Markup('Language <strong>' + str(lang_name) + '</strong> already exist!'))
            flash('danger')
            return redirect(url_for('languages.langs'))

        new_lang = Language(lang_name=lang_name, lang_code=lang_code)

        db.session.add(new_lang)
        db.session.commit()

        flash(Markup('Language <strong>' + lang_name + '</strong> was succussfully added!'))
        flash('success')
        return redirect(url_for('languages.langs')) 
    except Exception as ex:
        print('*** ' + str(datetime.now()) + ' *** language_post msg: ' + str(ex))
        logger.error(f"language_post msg: {ex}")
        return redirect(url_for('errors.unknownerror'))

@languages.route('/dlang/<id>', methods=['GET', 'POST'])
@login_required
def dlang(id):
    try:
        lang = Language.query.filter_by(id=id).first()
        name = lang.lang_name
        translations = Translation.query.filter_by(lang=lang.lang_code).all()
        for i in translations:
            db.session.delete(i)

        db.session.delete(lang)
        db.session.commit()
        flash(Markup('Language <strong>' + str(name) + '</strong> was deleted! All translations that were made in this language '+
        'have been moved removed'))
        flash('success')
        return redirect(url_for('languages.langs'))
    except Exception as ex:
        print('*** ' + str(datetime.now()) + ' *** dlang msg: ' + str(ex))
        logger.error(f"dlang msg: {ex}")
        return redirect(url_for('errors.unknownerror'))

@languages.route('/ulang/<id>', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def ulang(id):
    try:
        new_name = request.form.get('language_name')
        new_code = request.form.get('language_code')
        duplicate_langs = Language.query.filter_by(lang_name=new_name).all()
        duplicate_codes = Language.query.filter_by(lang_code=new_code).all()
        if duplicate_langs or duplicate_codes:
            flash(Markup('Language <strong>' + str(new_name) + '</strong> already exist!'))
            flash('danger')
            return redirect(url_for('languages.langs'))

        lang = Language.query.filter_by(id=id).first()
        old_name = lang.lang_name
        old_code = lang.lang_code
        lang.lang_name = new_name
        lang.lang_code = new_code
        db.session.commit()
        flash(Markup('Language <strong>' + str(old_name) + ' (' + str(old_code) + ')</strong> was renamed to '+
                    '<strong>' + new_name +' (' + str(new_code) + ')</strong>!'))
        flash('success')
        return redirect(url_for('languages.langs'))
    except Exception as ex:
        print('*** ' + str(datetime.now()) + ' *** ulang msg: ' + str(ex))
        logger.error(f"ulang msg: {ex}")
        return redirect(url_for('errors.unknownerror'))