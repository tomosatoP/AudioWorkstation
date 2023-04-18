# Sphinx を使った API 仕様書の作成
https://www.sphinx-doc.org/ja/master/index.html
## Sphinx のインストールと、プロジェクトの基本設定
~~~sh
(venv) ~/AudioWorkstation $ pip install Sphinx
(venv) ~/AudioWorkstation $ sphinx-quickstart docs
# > ソースディレクトリとビルドディレクトリを分ける（y / n）[n]:y
# > プロジェクト名: AudioWorkstation
# > 著者名（複数可）: tomosatoP
# > プロジェクトのリリース []: 1.0.0
# > プロジェクトの言語 [en]: ja
~~~
## apidoc ファイルの作成
~~~sh
(venv) ~/AudioWorkstation $ sphinx-apidoc -f -o docs/source src/audioworkstation --tocfile srcmodules
(venv) ~/AudioWorkstation $ sphinx-apidoc -f -o docs/source tests --tocfile testmodules
~~~
## 定義ファイルの編集
~~~diff
(venv) ~/AudioWorkstation $ nano docs/source/conf.py
- extensions = []
+ extensions = [
+     "sphinx.ext.autodoc",
+     "sphinx.ext.viewcode",
+     "sphinx.ext.todo",
+     "sphinx.ext.napoleon",
+     "sphinx.ext.githubpages",
+ ]
+ autodoc_typehints = "description"  # 型ヒントを有効
+ autoclass_content = "both"  # __init__()も出力
+ autodoc_default_options = {
+     "private-members": False,  # プライベートメソッドを表示しない
+     "show-inheritance": True,  # 継承を表示
+ }

(venv) ~/AudioWorkstation $ nano docs/source/index.rst
  .. toctree::
     :maxdepth: 2
     :caption: Contents:
  
+    srcmodules
+    testmodules
~~~
## API 仕様書(html)の作成
~~~sh
(venv) ~/AudioWorkstation $ sphinx-build -M html docs/source docs/build
(venv) ~/AudioWorkstation $ chrome docs/build/html/index.html
~~~
---
(venv) ~/AudioWorkstation $ pip install coverage
