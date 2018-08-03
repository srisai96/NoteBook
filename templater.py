import os
import jinja2

JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


def render_signup_page(**kwargs):
    template = JINJA_ENV.get_template('sign-up.html')
    kwargs['userSignedIn'] = False
    return template.render(**kwargs)


def render_signin_page(**kwargs):
    template = JINJA_ENV.get_template('sign-in.html')
    kwargs['userSignedIn'] = False
    return template.render(**kwargs)


def render_welcome_page(**kwargs):
    template = JINJA_ENV.get_template('welcome.html')
    return template.render(**kwargs)


def render_a_post(**kwargs):
    template = JINJA_ENV.get_template('a-post.html')
    # by default edit button will not be shown
    kwargs['showEdit'] = 'showEdit' in kwargs
    return template.render(**kwargs)


def render_all_post(**kwargs):
    template = JINJA_ENV.get_template('all-posts.html')
    return template.render(**kwargs)


def render_new_post(**kwargs):
    template = JINJA_ENV.get_template('new-post.html')
    return template.render(**kwargs)


def render_edit_post(**kwargs):
    template = JINJA_ENV.get_template('edit-post.html')
    # if this template is called to render i.e. user is already logged in
    kwargs['userSignedIn'] = True
    return template.render(**kwargs)

def render_friends(**kwargs):
    template = JINJA_ENV.get_template('friends.html')
    # if this template is called to render i.e. user is already logged in
    kwargs['userSignedIn'] = True
    return template.render(**kwargs)

def render_friendprofile(**kwargs):
    template = JINJA_ENV.get_template('friendprofile.html')
    # if this template is called to render i.e. user is already logged in
    kwargs['userSignedIn'] = True
    return template.render(**kwargs)
