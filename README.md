# wiki.py
##概要
PythonでWikipediaからテキスト情報を集める．  
[Wikipedia SandBox](http://ja.wikipedia.org/w/api.php)にアクセスしてWikipediaの記事を保存する．  
rivisionの指定もできるが，最新記事のみを収集．  
機能は最小限に抑える．
##使い方
基本的な使い方はsample.pyを参照．
sample1.py (アニメタイトル一覧の取得)
sample2.py (アニメ記事内容の取得)
sample3.py (アニメのあらすじ取得)
```python
# Sample code.
from wiki import Wiki

wiki = Wiki()
wiki.set_query("初音ミク")      # 対象を設定
content = wiki.get_content()    # 設定したwikipediaページのテキスト情報を取得
print content
```
