# Sphinx を使った API 仕様書の作成
https://www.sphinx-doc.org/ja/master/index.html
## Sphinx のインストールと、プロジェクトの基本設定
~~~sh
(venv) ~/AudioStation $ pip install Sphinx
(venv) ~/AudioStation $ sphinx-quickstart docs
# ソースとビルドのフォルダを分ける
# プロジェクト名
# 作者名
# プロジェクトバージョン
# プロジェクト自然言語
~~~
## apidoc ファイルの作成
~~~sh
(venv) ~/AudioStation $ sphinx-apidoc -f -o docs/source src/audioworkstation --tocfile srcmodules
(venv) ~/AudioStation $ sphinx-apidoc -f -o docs/source tests --tocfile testmodules
~~~
## 定義ファイルの編集
~~~diff
(venv) ~/AudioStation $ nano docs/source/conf.py
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

(venv) ~/AudioStation $ nano docs/source/index.rst
  .. toctree::
     :maxdepth: 2
     :caption: Contents:
  
+    srcmodules
+    testmodules
~~~
## API 仕様書(html)の作成
~~~sh
(venv) ~/AudioStation $ make -C docs html
(venv) ~/AudioStation $ open docs/build/html/index.html
~~~
---
(venv) ~/AudioStation $ pip install coverage
