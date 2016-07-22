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
    flag = True
    bTable = bool(cli.args.table)
    bScore = bool(cli.args.score)
    bScorers = bool(cli.args.scorers)
    url_dict = {}
    facts_tail = []

    if not bTable and not bScore and not bScorers and not bNews:
        bScore = True

    while True:
        try:
            os.system('clear')
            for k in cli.args.League:
                # Code to fetch data from URL[k]

                print(' ... Fetching information from www.livescore.com ... ')
                if lsweb.is_connected(pingTest) is True:

                    if bTable:
                        print("Displaying Table for {}".format(URL.URL[k][0]))
                        lsprint.table(lsweb.get_table(URL.URL[k][1]), k)

                    if bScore:
                        if index_no == 0:
                            print("Displaying Scores for {}".format(URL.URL[k][0]))
                            url_dict = lsprint.scores(lsweb.get_score(URL.URL[k][1]), k)
                            flag = True

                        elif index_no in url_dict.iterkeys():
                            print("Displaying Match Details for {} vs {}".format(url_dict[index_no][1],url_dict[index_no][2]))
                            lsprint.match_facts('http://livescore.com'+url_dict[index_no][0], facts_tail)
                            flag = False

                        else:
                            print(c.RED+'Index number not in range')
                            url_dict = lsprint.scores(lsweb.get_score(URL.URL[k][1]), k)
                            flag = True

                    if bScorers:
                        print("Displaying Top Scorers for"
                              " {}".format(URL.URL[k][0]))
                        print('Working on it')

                else:
                    print(c.fill[3]+"Check Your Internet Connection ,"
                          " It looks like you're out of internet."+c.END)

                time.sleep(3)

            bTable = False
            bScorers = False
            if not bool(bScore):
                break
            time.sleep(7)

        except KeyboardInterrupt:

            try:
                if len(url_dict) > 0 and flag == True:

                    facts_input = raw_input(c.CYAN+" Enter index number of the match: "+c.END)
                    _temp = facts_input.split(' ')
                    index_no = int(_temp[0])
                    facts_tail = _temp[1]

                elif len(url_dict) > 0 and flag == False:
                    main()


                else:
                    print(c.RED+'\n\nBye, Keep Loving Football and livescore-cli :)\n')
                    break



            except KeyboardInterrupt:

                print(c.RED+'\n\nBye, Keep Loving Football and livescore-cli :)\n')
                break

if __name__ == '__main__':
    main()
