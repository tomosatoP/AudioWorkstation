# Sphinx を使った API 仕様書の作成
https://www.sphinx-doc.org/ja/master/index.html

## Sphinx のインストールと、プロジェクトの基本設定
~~~sh
(venv) ~/AudioWorkstation $ pip install Sphinx
(venv) ~/AudioWorkstation $ sphinx-quickstart shinx
# > ソースディレクトリとビルドディレクトリを分ける（y / n）[n]:y
# > プロジェクト名: AudioWorkstation
# > 著者名（複数可）: tomosatoP
# > プロジェクトのリリース []: 1.0.0
# > プロジェクトの言語 [en]: ja
~~~
## apidoc ファイルの作成
~~~sh
(venv) ~/AudioWorkstation $ sphinx-apidoc -f -o sphinx/source src/audioworkstation --tocfile srcmodules
(venv) ~/AudioWorkstation $ sphinx-apidoc -f -o sphinx/source tests --tocfile testmodules
~~~
## 定義ファイルの編集
~~~diff
(venv) ~/AudioWorkstation $ nano sphinx/source/conf.py
- extensions = []
+ extensions = [
+     "sphinx.ext.autodoc",
+     "sphinx.ext.viewcode",
+     "sphinx.ext.todo",
+     "sphinx.ext.napoleon",
+     "sphinx.ext.githubpages",
+ ]
+ add_module_names = False           # オブジェクト名の前にモジュール名を付けない
+ autodoc_member_order = "groupwise" # メンバーのタイプに応じてソートを変更
+ autodoc_typehints = "description"  # 型ヒントを有効
+ autoclass_content = "both"         # __init__()も出力
+ autodoc_default_options = {
+     "private-members": False,      # プライベートメソッドを表示しない(デフォルト)
+     "show-inheritance": True,      # 継承を表示
+ }

(venv) ~/AudioWorkstation $ nano sphinx/source/index.rst
  .. toctree::
     :maxdepth: 2
     :caption: Contents:
  
+    srcmodules
+    testmodules
~~~
## API 仕様書(html)の作成
~~~sh
(venv) ~/AudioWorkstation $ make -C sphinx clean
(venv) ~/AudioWorkstation $ sphinx-build -b html sphinx/source docs
# "-M" とは出力先のフォルダ構成が異なる
(venv) ~/AudioWorkstation $ chrome docs/index.html
~~~
---
(venv) ~/AudioWorkstation $ pip install coverage
