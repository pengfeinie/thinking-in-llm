# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'thinking-in-LLM'
copyright = '2024, pfnie'
author = 'pfnie'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
     'recommonmark',
     'sphinx_markdown_tables',
     'sphinxcontrib.video',
     'sphinx.ext.autodoc',
     'sphinx.ext.viewcode',
     'sphinx.ext.githubpages',
     'rst2pdf.pdfbuilder'
 ]

templates_path = ['_templates']
exclude_patterns = []

# add "Edit on Github"
html_context = {
	"display_github": True,
	"github_user":"pengfeinie",
	"github_repo":"thinking-in-LLM",
	"github_version":"main/source/"
}



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# If true, links to the reST sources are added to the pages.
#
html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#
html_show_sphinx = True
