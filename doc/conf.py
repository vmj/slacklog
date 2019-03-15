# -*- coding: utf-8 -*-

# This is for autodoc and for reusing the constants like version
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

import slacklog

project = u'slacklog'
copyright = u'2019, Mikko Värri'
author = u'Mikko Värri'

# The short X.Y version.
version = slacklog.__version__
# The full version, including alpha/beta/rc tags.
release = slacklog.__version__

needs_sphinx = '1.8.5'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode'
]

# http://www.sphinx-doc.org/en/stable/theming.html
html_theme = 'nature'
