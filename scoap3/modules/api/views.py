from __future__ import absolute_import, print_function

from flask import Blueprint, render_template, request, flash
from invenio_accounts.models import User

from .models import ApiRegistrations

from invenio_db import db

blueprint = Blueprint(
    'scoap3_api',
    __name__,
    url_prefix='/partners',
    template_folder='templates',
    static_folder='static',
)


@blueprint.route('/')
def index():
    return render_template(
        'scoap3_api/index.html',
        title='SCOAP3 Repository - API'
    )


def handler_registration():
    if request.method != 'POST':
        return False

    email = request.form.get('email')

    if not email:
        flash('Please provide a valid email address!', 'error')
        return False

    already_exists = User.query.filter(User.email == email).count()
    if already_exists:
        flash("User with email '%s' is already registered." % email, 'error')
        return False

    request_already_exists = ApiRegistrations.query.filter(ApiRegistrations.email == email).count()
    if request_already_exists:
        flash("Registration failed! Request with email '%s' already exists." % email, 'error')
        return False

    new_reg = ApiRegistrations(partner=bool(int(request.form.get('partner', '0'))),
                               name=request.form.get('name', ''),
                               email=email,
                               organization=request.form.get('organization', ''),
                               role=request.form.get('role', ''),
                               country=request.form.get('country', ''),
                               description=request.form.get('description', '')
                               )
    db.session.add(new_reg)
    db.session.commit()
    flash("Registration successful. You will receive an email as soon as your account gets approved.",
          'message')

    return True


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    handler_registration()

    return render_template(
        'scoap3_api/register.html',
        title='SCOAP3 Repository - Tools registration',
    )
