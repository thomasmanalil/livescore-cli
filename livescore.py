#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, time
from lib import lscolors as c
from lib import cli
from lib import URL
from lib import lsprint
from lib import lsweb
from lib import lsnews


def main():
    pingTest = 'www.google.com'
    index_no = 0
    flag = 0
    bTable = bool(cli.args.table)
    bScore = bool(cli.args.score)
    bScorers = bool(cli.args.scorers)
    url_dict = {}
    facts_tail = []
    bye_message = '\n\nBye, Keep Loving Football and livescore-cli :)\n'

    if not bTable and not bScore and not bScorers and not bNews:
        bScore = True

    while True:
        try:
            os.system('clear')
            for k in cli.args.League:
                # Code to fetch data from URL[k]
                print(' ... Fetching information from www.livescore.com ... ')
                if lsweb.is_connected(pingTest) is True:
                    content = lsweb.get_content_ts(lsweb.get_soup(URL.URL[k][1]))

                    if bTable:
                        print("Displaying Table for {}".format(URL.URL[k][0]))
                        lsprint.table(lsweb.get_table(content), k)

                    if bScore:
                        if index_no == 0:
                            print("Displaying Scores for {}".format(URL.URL[k][0]))
                            url_dict = lsprint.scores(lsweb.get_score(content), k)
                            flag = 0

                        elif index_no in url_dict.iterkeys():
                            print("Displaying Match Details for {} vs {}".format(url_dict[index_no][1],url_dict[index_no][2]))
                            lsprint.match_facts('http://livescore.com'+url_dict[index_no][0], facts_tail)
                            flag = 1

                        else:
                            print(c.RED+'Index number not in range')
                            url_dict = lsprint.scores(lsweb.get_score(content), k)
                            flag = 0

                    if bScorers:
                        print("Displaying Top Scorers for"
                              " {}".format(URL.URL[k][0]))
                        print('Working on it')

                else:
                    flag = 1
                    print(c.TITLE+"Check Your Internet Connection,"
                          " It looks like you're out of internet."+c.END)

                time.sleep(3)

            bTable = False
            bScorers = False
            if not bool(bScore):
                break
            time.sleep(7)

        except KeyboardInterrupt:

            try:
                if url_dict and flag == 0:

                    facts_input = raw_input(c.CYAN+" Enter index number of the match: "+c.END)
                    _temp = facts_input.split(' ')
                    index_no = int(_temp[0])
                    facts_tail = _temp[1]

                elif url_dict and flag == 1:
                    index_no = 0

                else:
                    print(c.GREEN+bye_message+c.END)
                    flag = 0
                    break


            except KeyboardInterrupt:
                print(c.GREEN+bye_message+c.END)
                break

if __name__ == '__main__':
    main()
