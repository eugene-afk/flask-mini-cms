from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def page_not_found(err):
    return render_template('error.html', title='Page not found',
     msg='What you were looking for is just not there.'), 404

@errors.app_errorhandler(403)
def forbidden(err):
    return render_template('error.html', title='Forbidden',
     msg='This page is forbidden.'), 403

@errors.app_errorhandler(410)
def gone(err):
    return render_template('error.html', title='Page Gone',
     msg='This page no longer exists.'), 410

@errors.app_errorhandler(500)
def internal_server_error(err):
    return render_template('error.html', title='Internal Server Error',
     msg='Server overloaded or not respond, try to refresh page latter.'), 500

@errors.route('/unknownerror')
def unknownerror():
    return render_template('error.html', title='Unknown Error',
           msg="Occured one or more unknown exception(s). Contact with administrator or try again later.")