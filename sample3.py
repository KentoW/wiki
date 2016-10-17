# -*- coding: utf-8 -*-
# サンプルコード3
# サンプルコード2で作成したwikipediaのアニメ記事からあらすじだけ抽出する
# 要：MeCabモジュール
import sys
import re
import MeCab

tagger = MeCab.Tagger()

p = re.compile(ur"\[(.+)\|(.+)\]")


def main():
    database = []
    for strm in open("./anime_wiki_contents.txt", "r"):
        if strm.startswith("@boc"):
            data = {"title": strm.strip().split(":")[1]}
            data["content"] = []
        elif strm.startswith("@eoc"):
            database.append(data)
        else:
            data["content"].append(strm.strip())


    out = {}
    for data in database:
        flag = 0
        flag2 = 0
        flag3 = 0
        view = {"title": data["title"], "story": []}
        for line in data["content"]:
            if line.startswith(("== ストーリー", "==ストーリー", "=== ストーリー", "===ストーリー", "== あらすじ", "=== あらすじ", "==あらすじ", "===あらすじ")):
                flag = 1
            elif flag == 1:
                if line.startswith("{{要あらすじ"):
                    break
                if line.startswith("="):
                    if flag3 == 1:
                        flag2 += 1
                if line.startswith(("=", "{", ";", "<", "*", "※", "|")):
                    continue
                elif line == "":
                    continue
                elif len(unicode(line)) < 50:
                    continue
                else:
                    article = "".join(line.split("'"))
                    article = re.sub(ur"\|(.+)\]", "]", unicode(article))
                    article = re.sub(ur"[\], \[, #]", "", unicode(article))
                    article = re.sub(ur"（.+）", "", unicode(article))
                    article = re.sub(ur"<.+>.+</.+>", "", unicode(article))
                    article = re.sub(ur"<.+>", "", unicode(article))

                    article = article.encode("utf8")
                    if article.startswith(":"):
                        article = "".join(article.split(":")[1::])
                    if len(unicode(article)) < 40:
                        continue
                    if flag2 == 1:
                        flag = 0
                        L = []
                        for sentence in view["story"]:
                            for morph in tagger.parse(sentence.encode('utf-8')).split('\n'):
                                info = morph.split("\t")
                                if len(info) > 1:
                                    sur = info[0]
                                    pos = info[1].split(",")[0]
                                    if pos != "記号":
                                        L.append(sur)
                        out[view["title"]] = " ".join(L)
                        break
                    if article:
                        flag3 = 1
                        view["story"].append(article)
    for title, line in out.iteritems():
        print "#", title
        print line


if __name__ == "__main__":
    main()

