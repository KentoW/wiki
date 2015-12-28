# -*- coding: utf-8 -*- 
# Wikipedia SandBox から json形式で色々抽出するスクリプト
import sys
import urllib2
import json as js

class Wiki():
    def __init__(self):
        self.url = "http://ja.wikipedia.org/w/api.php?"
        self.query = "メインページ"
        self.param = "action=query&prop=revisions&format=json&rvprop=content&rvlimit=1&titles=%s&redirects=" %(urllib2.quote(self.query))

    def set_query(self, query):
        self.query = query
        self.param = "action=query&prop=revisions&format=json&rvprop=content&rvlimit=1&titles=%s&redirects=" %(urllib2.quote(self.query))

    def get_content(self):
        res = urllib2.urlopen(self.url + self.param)
        json = js.loads(res.read())
        if "-1" in json["query"]["pages"]:
            sys.stderr.write("error: page \"%s\" is not found.\n"%(self.query))
            return None
        else:
            for page_num in json["query"]["pages"]:
                for revision in json["query"]["pages"][page_num]["revisions"]:
                    return revision["*"]
                    break   #revisonは一つだけで(つまり最新版)を取得

def main():
    wiki = Wiki()
    wiki.set_query("初音ミク")
    print wiki.get_content()

if __name__ == "__main__":
    main()
