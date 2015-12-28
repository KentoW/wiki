# wiki.py
##概要
PythonでWikipediaからテキスト情報を集める．  
[Wikipedia SandBox](http://ja.wikipedia.org/w/api.php)にアクセスしてJSON形式としてWikipediaの記事を保存する．  
rivisionの指定もできるが，最新記事のみを収集．  
機能は最小限に抑える．
##使い方
基本的な使い方はsample.pyを参照．
```python
# Sample code.
from wiki import Wiki

wiki = Wiki()
wiki.set_query("初音ミク")      # 対象を設定
wiki_json = wiki.get_content()  # 設定したwikipediaページのJSONを取得
print wiki_json
```
