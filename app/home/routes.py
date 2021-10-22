'''
Author: Dilision
Date: 2021-05-26 11:38:11
Description: 
'''
# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, request,Flask
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
import os
from flask_uploads import UploadSet, configure_uploads, ARCHIVES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from app.home.util import UploadForm, firmware


@blueprint.route('/upload.html', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        filename = firmware.save(form.firmware.data)
        name=form.name.data
        brand=request.form.get('brand')
        info=form.info.data
    return render_template('upload.html', form=form, data=[{'name':'D-Link'}, {'name':'TP-Link'}, {'name':'TrendNet'}, {'name':'Cisco'},  {'name':'Netgear'},  {'name':'Tenda'}, {'name':'Belkin'}, {'name':'other'}])

@blueprint.route('/index')
@login_required
def index():

    return render_template('index.html', segment='index')

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith( '.html' ):
            template += '.html'

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( template, segment=segment )

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500

# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None  
