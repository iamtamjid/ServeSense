# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here.
import os
import sys
# This line tells Sphinx to look one level up from the 'source' directory,
# then into our main project folder to find our code.
sys.path.insert(0, os.path.abspath('../../'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'ServeSense.settings' 
import django
django.setup()



project = 'ServeSense'
copyright = '2025, Mohaimen Azad, Tamjid Islam'
author = 'Mohaimen Azad, Tamjid Islam'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',      # The most important one: pulls docstrings from code
    'sphinx.ext.viewcode',     # Adds links to your source code from the docs
    'sphinx.ext.napoleon',     # Can understand Google and NumPy style docstrings
    'sphinx_rtd_theme',        # Enables the Read the Docs theme
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
