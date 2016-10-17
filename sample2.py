# -*- coding: utf-8 -*-
# wiki.pyのサンプルコード2
# sample.pyで手に入れたアニメタイトル一覧に掲載されているアニメのwikipediaページの内容を全部保存する
import sys
import argparse
from wiki import Wiki


class Collect:
    def __init__(self):
        self.wiki = Wiki()
        self.title = ""
        self.content = []

    def collect_content(self, title):
        self.title = title
        self.wiki.set_query(self.title)
        content = self.wiki.get_content()
        if content: 
            self.content = content.strip().split("\n")
            print "@boc:%s"%(title)
            print "\n".join(self.content)
            print "@eoc:%s"%(title)
            sys.stderr.write(title + "\n")

def main(args):
    coll = Collect()
    for strm in open(args.title, "r"):
        title = strm.strip().split("\t")[7]
        coll.collect_content(title)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--title', dest='title', default="anime_list.tsv", type=str, help='specify tsv file of anime list')
    args = parser.parse_args()
    main(args)
