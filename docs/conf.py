# Configuration file for the Sphinx documentation builder.

import os
import sys
sys.path.insert(0, os.path.abspath('../myproject'))

# Project information
project = 'Todo API'
copyright = '2024, Your Name'
author = 'Your Name'
release = '0.1.0'

# Extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

# Templates path
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# HTML theme
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Django configuration
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'
django.setup()
