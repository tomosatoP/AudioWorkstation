# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "AudioWorkstation"
copyright = "2023, tomosatoP"
author = "tomosatoP"
release = "0.3"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.todo",
    "sphinx.ext.napoleon",
    "sphinx.ext.githubpages",
]
add_module_names = False
autodoc_typehints = "description"  # 型ヒントを有効
autoclass_content = "both"  # __init__()も出力
autodoc_default_options = {
    "private-members": False,  # プライベートメソッドを表示しない
    "show-inheritance": True,  # 継承を表示
}
templates_path = ["_templates"]
# exclude_patterns = []

language = "ja"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinxdoc"
html_static_path = ["_static"]
