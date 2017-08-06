#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import lsweb
import lsprocess
import lsprint
import lscolors
import URL
import tt
import json


def read_json(file_path):
    with open(file_path) as f:
        json_read = json.load(f)
    return json_read


def write_json(file_path, dict_file, dict_indent=4):
    with open(file_path, "w") as f:
        f.write(json.dumps(dict_file))


def get_news(url=URL.goalUS, sclass='news_box2'):
    news_dict = {}
    try:
        rows = lsweb.get_livescore(url, sclass)
        contents = '\n'.join(map(lambda r: r.text, rows))
        news = contents.split("\n")
        news_dict = {"news": news, "last_updated_time": tt.datetime_now()}
        write_json("data.json", news_dict)

    except Exception as e:
        if "connection" in str(e).lower():
            news_dict = read_json("data.json")

    return news_dict


def print_news(news_dict):
    last_updated_time = news_dict.get("last_updated_time")
    news_array = news_dict.get("news")
    print('fetching soccer news from goal.com...\n')
    print('(Last Updated at ' + lscolors.ORANGE + last_updated_time + lscolors.END + ')')

    width = lsprocess.find_longest_no(news_array)
    lsprint.print_pattern('*', width+6, lscolors.ORANGE)

    for sn, each_news in enumerate(news_array):
        print(lscolors.colorArray[sn%2+2] + ''.join(each_news.ljust(5)))

    lsprint.print_pattern('*', width+6, lscolors.ORANGE)
    #print(" Press Ctrl+C to exit, If you're done :) ")
    lsprint.print_pattern('*', width+6, lscolors.ORANGE)


if __name__ == '__main__':
    print_news(get_news())
