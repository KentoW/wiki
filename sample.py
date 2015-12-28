# -*- coding: utf-8 -*-
# wiki.pyのサンプルコード
# wikipediaからアニメタイトル一覧を取得する
# wikipediaから取得するのはただのテキストなので，正規表現などを駆使して，必要な情報のみを抽出する．
# 属性として title, sub_title, cool, start_date, end_date, company, station, story を タブ区切りで出力
# 一期，二期の区別はしない．(wikipediaのページは一期と二期の区別をしていないため) 
# クールは冬:2014-1, 春:2014-2, 夏:2014-3, 秋:2014-4 とする
import re
from wiki import Wiki


def get_anime_list():
    anime_list = []
    head_kanas = ["(2010年代 後半)", "(2010年代 前半)", "(2000年代 後半)", "(2000年代 前半)", "(1990年代)", "(1980年代)", "(1970年代)", "(1960年代)"]
    anime = Wiki()
    for head_kana in head_kanas[::-1]:
        anime.set_query("日本のテレビアニメ作品一覧 %s"%(head_kana))
        content =  anime.get_content()
        for line in content.strip().split("\n"):
            if line.startswith("=="):
                year = unicode(line.strip("=*").strip())
                if len(year.split(" ")) > 1:
                    start_year = unicode(year)[:4:].encode("utf8")
            if len(line.split("||")) == 5:
                info = line.split("||")

                # Step1: date
                start_end = info[0].lstrip("|").split("-")
                start_date = re.split(ur"\(|（|・|、", unicode(start_end[0].strip()))[0]
                ymd = re.split(ur"年|月|日", unicode(start_date))
                if len(ymd) == 4:   # 年が入っていない場合
                    start_year = ymd[0]
                    start_month = ymd[1]
                    start_day = ymd[2]
                elif len(ymd) == 3: # 年が入っていないもの
                    start_month = ymd[0]
                    start_day = ymd[1]
                if len(start_end) == 1: # 開始日しかないもの(多分特番やOVA)
                    end_year = start_year
                    end_month = start_month
                    end_day = start_day
                else:   # 終了日もあるもの
                    end_date = re.split(ur"\(|（|・|、", unicode(start_end[1].strip()))[0]
                    ymd = re.split(ur"年|月|日", unicode(end_date))
                    if len(ymd) == 4:   # 年が入っていない場合
                        end_year = ymd[0]
                        end_month = ymd[1]
                        end_day = ymd[2]
                    elif len(ymd) == 3: # 年が入っていないもの
                        end_year = start_year
                        end_month = ymd[0]
                        end_day = ymd[1]
                    elif len(ymd) == 1:  # まだ終了していないもの
                        end_year = "null"
                        end_month = "null"
                        end_day = "null"

                # Step2: cool   面倒だから開始クール=クールにする   改良の余地あり
                if start_month in ("1", "2", "3"):
                    cool = "%s-%s"%(start_year, 1)
                elif start_month in ("4", "5", "6"):
                    cool = "%s-%s"%(start_year, 2)
                elif start_month in ("7", "8", "9"):
                    cool = "%s-%s"%(start_year, 3)
                elif start_month in ("10", "11", "12"):
                    cool = "%s-%s"%(start_year, 4)

                # Step3: title, sub_title
                titles = re.split(ur"\[\[|\]\]", unicode(info[1]))[1].split("|")
                if len(titles) == 2:
                    title = titles[0]
                    sub_title = titles[1]
                else:
                    title = titles[0]
                    sub_title = "null"

                # Step4: company
                companys = []
                for comp in info[2].split("、"):
                    if comp.endswith("</ref>"):
                        continue
                    companys.append(comp.strip("[[\]]").split("|")[0])
                company = ",".join(companys)

                # Step5: station
                stations = []
                for stat in info[3].split("、"):
                    stations.append(stat.strip("[[\]]").split("|")[0])
                station = ",".join(companys)

                # Step6: story
                story = info[4].split("<")[0].strip().lstrip("全").rstrip("話")
                if story in ("", "-", "カウント不能", "放送中"):
                    story = "null"
                anime_list.append("\t".join([start_year, start_month, start_day, end_year, end_month, end_day, cool, title, sub_title, company, station, story]))
    return anime_list


def main():
    anime_list = get_anime_list()
    print "\n".join(anime_list)


if __name__ == "__main__":
    main()
