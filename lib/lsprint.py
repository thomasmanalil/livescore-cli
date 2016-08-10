#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
    modules containg all the layout configuration of printable data
    scores : function containing layout info of scores
    table : function containing layout info of table
'''

import lscolors as c
import subprocess
import sys, os
import tt, URL, lsprocess
import lsweb


def sendAlert(message,title=''):
    #path to icon png file
    icon_path = '/usr/share/icons/livescore.png'
    #bash command to send notification
    bash_command = 'notify-send -i '+icon_path+' "'+title+'" "'+message+'"'
    os.system(bash_command)
    return


facts_route = {}

#global variable to temporarily store the score of home and away team to compare for notification
score_h = [0]*50
score_a = [0]*50

def scores(scores,key):
    global score_h, score_a, facts_route
    lmax = lsprocess.get_longest_list(scores)
    total_width = sum(lmax)+11; test = 3
    index_no = 0    #temporary value to count match with link

    print_pattern('-',total_width,c.BLUE)
    print(c.TITLE+'\t\t\t '+URL.URL[key][0]+' SCORES \t\t\t'+c.END)
    print_pattern('-',total_width,c.BLUE)

    for position,each_row in enumerate(scores):
        if isinstance(each_row,list) == False:
            #extract date if 1D array
            date = each_row.strip()
            date_color = c.dateArray[test%3]; test+=1
        else:
            #time conversion to local time
            time = tt._convert(each_row[0].strip())

            home_team = each_row[1].strip()
            home_team_color = c.GREEN
            away_team = each_row[3].strip()
            away_team_color = c.GREEN

            try:
                if isinstance(each_row[2],list) == False:

                    _temp = each_row[2].strip().split()
                    home_team_score = int(_temp[0])
                    away_team_score = int(_temp[2])
                    temp_index = '  '

                else:
                    _temp = each_row[2][0].strip().split()
                    home_team_score = int(_temp[0])
                    away_team_score = int(_temp[2])
                    index_no = index_no + 1
                    temp_index = str(index_no)
                    facts_route[index_no] = [(each_row[2][1].strip()), home_team, away_team]

                middle_live = str(home_team_score) + ' - ' + str(away_team_score)

                if home_team_score > away_team_score:
                    away_team_color = c.RED
                    home_team_color = c.ORANGE
                elif home_team_score < away_team_score:
                    away_team_color = c.ORANGE
                    home_team_color = c.RED
                else:
                    away_team_color = c.CYAN
                    home_team_color = c.CYAN

                #if previous score is not equal to present score send notification to user
                if home_team_score != score_h[position] or away_team_score != score_a[position]:
                    #sendAlert(time+'   ' + home_team + '  ' + middle_live + '  ' + away_team,key)
                    score_h[position] = home_team_score
                    score_a[position] = away_team_score

            except:
                if isinstance(each_row[2],list) == False:
                    middle_live = each_row[2].strip()
                    temp_index = '  '

                else:
                    middle_live = each_row[2][0].strip()
                    index_no = index_no + 1
                    temp_index = str(index_no)
                    facts_route[index_no] = (each_row[2][1].strip(), home_team, away_team)


            print(' '+date_color+''.join((temp_index).ljust(2))+' '
                    +''.join(date.ljust(lmax[0])) + ''.join(time.ljust(lmax[1]+2))      \
                    + c.END +home_team_color+''.join(home_team.ljust(lmax[2]+2))+c.END  \
                    + ''.join(middle_live.ljust(lmax[3]+2)) + away_team_color           \
                    + ''.join(away_team.ljust(lmax[4])) + c.END)

    print_pattern('-',total_width,c.BLUE)
    if temp_index != '  ':
        print('Ctrl+C & ENTER RESPECTIVE NUMBER & DETAILTYPE FOR MATCH DETAILS\n\
                i.e. '+c.CYAN+'1 lineup \t'+c.END+'for viewing lineups if exists\n\
                or   '+c.CYAN+'1 details \t'+c.END+'for match details if exists\n\
                or  '+c.CYAN+' 1 statistics \t'+c.END+'for match statistics if exists')

    print_pattern('-',total_width,c.BLUE)
    return facts_route


def match_facts(url, flag):

    details, lineup, statistics = lsweb.get_match_facts(url)

    if flag.strip() == 'details':
        _details(details)

    elif flag.strip() == 'lineup':
        _lineup(lineup)

    elif flag.strip() == 'statistics':
        if len(statistics) == 0:
            print('No Statistics Found')

        else:
            print(Statistics)

    else:
        print('Only details, lineup & statistics are valid ... ')



def _lineup(lineups):

    lengthlist = lsprocess.get_longest_list(lineups)
    length = max(lengthlist)+2
    plen = int(length*3-length/5)
    print_pattern('+',plen,c.BLUE)
    print(c.TITLE+'\t\t\t'+' LINEUPS '+c.END)
    print_pattern('+',plen,c.BLUE)

    flag = 0 #flag for details like lineup, substitution etc
    print(c.ORANGE+'       '+''.join(('HOME TEAM').ljust(length)) \
            +'      '+''.join(('AWAY TEAM').ljust(length))+c.END)

    print_pattern('-',plen,c.BLUE)

    for each_row in lineups:
        if isinstance(each_row, list) == False:
            if each_row == 'line-ups :':
                flag = 1

            elif each_row == 'substitutions :':
                print_pattern('*',plen,c.BLUE)
                print(c.ORANGE+'\t\t\tPLAYER SUBSTITUTIONS')
                flag = 2

            elif each_row == 'substitute players :':
                print_pattern('~',plen,c.BLUE)
                print(c.ORANGE+'\t\t\tSUBSTITUTE PLAYERS')
                print_pattern('~',plen,c.BLUE)
                flag = 3

            elif each_row == 'coach :':
                print_pattern('*',plen,c.BLUE)
                print(c.ORANGE+'\t\t\tMANAGERS')
                print_pattern('-',plen,c.BLUE)
                flag = 4

            elif each_row == 'formations :':
                flag = 5


        else:

            if flag == 5:
                print('      '+''.join(str(each_row[0]).ljust(length)) \
                    +'      '+''.join(str(each_row[1]).ljust(length)))
                print_pattern('-',plen,c.BLUE)


            elif flag == 1:

                if len(each_row) == 2:
                    print(c.CYAN+'      '+''.join(each_row[0].ljust(length)) \
                            +'      '+''.join(each_row[1].ljust(length))+c.END)

                elif len(each_row) == 3:
                    try:
                        int((each_row[0].split("'"))[0])
                        print(' '+c.RED+''.join(each_row[0].ljust(5)) \
                                +''.join(each_row[1].ljust(length))+'      '+\
                                c.CYAN+''.join(each_row[2].ljust(length))+c.END)
                    except:
                        print('      '+c.CYAN+''.join(each_row[0].ljust(length))\
                                +' '+c.RED+''.join(each_row[1].ljust(5)) \
                                +''.join(each_row[2].ljust(length)))

                elif len(each_row) == 4:
                    print(' '+c.RED+''.join(each_row[0].ljust(5))\
                            +''.join(each_row[1].ljust(length)) \
                            +' '+c.RED+''.join(each_row[2].ljust(5)) \
                            +''.join(each_row[3].ljust(length)))


            elif flag == 4:
                print('      '+c.PURPLE+''.join(str(each_row[0]).ljust(length)) \
                    +'      '+''.join(str(each_row[1]).ljust(length)))

            elif flag == 2:
                try:
                    print_pattern('-',plen,c.BLUE)
                    print(' '+c.RED+''.join(each_row[0].ljust(5))\
                            +''.join(each_row[1][0].ljust(length))\
                            +' '+''.join(each_row[2].ljust(5))\
                            +''.join(each_row[3][0].ljust(length))\
                            +'(off)'+c.END)

                    print('      '+c.GREEN+''.join(each_row[1][1].ljust(length))\
                            +'      '+''.join(each_row[3][1].ljust(length))\
                            +'(on)'+c.END)

                except:
                    try:
                        print(' '+c.RED+''.join(' '.ljust(5))\
                                +''.join(' '.ljust(length))\
                                +' '+''.join(each_row[1].ljust(5))\
                                +''.join(each_row[2][0].ljust(length))\
                                +'(off)'+c.END)

                        print('      '+c.GREEN+''.join(' '.ljust(length))\
                                +'      '+''.join(each_row[2][1].ljust(length))\
                                +'(on)'+c.END)
                    except:
                        print(c.RED+' '+''.join(each_row[0].ljust(5))\
                                +''.join(each_row[1][0].ljust(length))\
                                +'(off)'+c.END)

                        print(c.GREEN+'      '+''.join(each_row[1][1].ljust(length))\
                                +'(on)'+c.END)


            elif flag == 3:

                if len(each_row) == 2:
                    print(c.CYAN+'      '+''.join(each_row[0].ljust(length)) \
                            +'      '+''.join(each_row[1].ljust(length))+c.END)

                elif len(each_row) == 3:
                    try:
                        int((each_row[0].split("'"))[0])
                        print(' '+c.GREEN+''.join(each_row[0].ljust(5)) \
                                +''.join(each_row[1].ljust(length))+'      '+\
                                c.CYAN+''.join(each_row[2].ljust(length))+c.END)
                    except:
                        print('      '+c.CYAN+''.join(each_row[0].ljust(length))\
                                +' '+c.GREEN+''.join(each_row[1].ljust(5)) \
                                +''.join(each_row[2].ljust(length)))

                elif len(each_row) == 4:
                    print(' '+c.GREEN+''.join(each_row[0].ljust(5))\
                            +''.join(each_row[1].ljust(length)) \
                            +' '+c.GREEN+''.join(each_row[2].ljust(5)) \
                            +''.join(each_row[3].ljust(length)))

    print_pattern('~',plen,c.BLUE)
    print_pattern('~',plen,c.BLUE)

def _details(details):
    plen = 70
    for detail in details:
        if len(detail) > 2:
            try:
                score = (detail[2]).strip().split(' - ')
                scoreh = int(score[0])
                scorea = int(score[1])
                print_pattern('~',plen,c.BLUE)
                if isinstance(detail[1],list) == False:
                    print(detail[0]+' '+ detail[1]+'\t'+score[0]+' - '+score[1])
                else:
                    print(detail[0]+' '+ detail[1][0]+' '+detail[1][1]\
                            +'\t'+score[0]+' - '+score[1])
            except:
                try:
                    score = (detail[1]).strip().split(' - ')
                    scoreh = int(score[0])
                    scorea = int(score[1])
                    print_pattern('~',plen,c.BLUE)
                    if isinstance(detail[1],list) == False:
                        print(detail[0]+' '+ detail[1]+'\t'+score[0]+' - '+score[1])
                        print('2')
                    else:
                        print(detail[0]+' '+ detail[1][0]+' '+detail[1][1]\
                                +'\t'+score[0]+' - '+score[1])
                        print('3')


                except:
                    print('0')


def table(tables,key):
    table = URL.URL[key][0]+' TABLE'
    league_position = 0
    _temp = lsprocess.get_longest_list([row[1] for row in tables])
    longest_length = int(_temp[0])
    ucl = 'Champions League';   ucl_color = c.ORANGE
    ucl_qual = 'Champions League qualification';    ucq_color = c.BLUE
    europa = 'Europa League';   eup_color = c.PURPLE
    europa_qual = 'Europa League qualification';    euq_color = c.CYAN
    rel = 'Relegation'; rel_color = c.RED

    print_pattern('+',75+longest_length,c.BLUE)
    print('\t\t\t\t'+c.GREEN+table)
    print_pattern('+',75+longest_length,c.BLUE)

    print(' LP'+'\t'+''.join('Team Name'.ljust(longest_length))    	\
            +'\t'+'GP'+'\t'+'W'+'\t'+'D'+'\t'+'L'+'\t'+'GF'+'\t'+'GA'   \
            +'\t'+'GD'+'\t'+'Pts')

    print_pattern('-',75+longest_length,c.BLUE)

    for first_row in tables[1::]:
        league_position += 1
        team_name = first_row[1]
        games_played = first_row[2]
        total_wins = first_row[3]
        total_draws = first_row[4]
        total_loses = first_row[5]
        goals_for = first_row[6]
        goals_against = first_row[7]
        goal_difference = first_row[8]
        total_points = first_row[9]

        row_color = c.GREEN
        if isinstance(first_row[0],list) == True:
            if first_row[0][1] == ucl:
                row_color = ucl_color
            elif first_row[0][1] == ucl_qual:
                row_color = ucq_color
            elif first_row[0][1] == europa:
                row_color = eup_color
            elif first_row[0][1] == europa_qual:
                row_color = euq_color
            elif first_row[0][1] == rel:
                row_color = rel_color

        else:
            pass

        print(row_color+' '+str(league_position)+'\t'    			\
                +''.join(team_name.ljust(longest_length))		 	\
                +'\t'+games_played+'\t'+total_wins+'\t'+total_draws+'\t'     	\
                +total_loses+'\t'+goals_for+'\t'+goals_against+'\t'     	\
                +goal_difference+'\t'+total_points+c.END)

    print_pattern('+',75+longest_length,c.BLUE)
    print(c.GRAY+' LP = League Position \tGP = Games Played\tW = Wins \tD = Draws \tL = Lose \n GF = Goals For\t\tGA = Goal Against \tGD = Goal Differences')
    print_pattern('-',75+longest_length,c.GREEN)
    print(' '+ucl_color+ucl+'\t'+ucq_color+ucl_qual+'\t'+eup_color+europa+'\n '+euq_color+europa_qual+'\t'+rel_color+rel)
    print_pattern('+',75+longest_length,c.BLUE)








def print_pattern(c2p,n,color): #characterToprint #no of character to print
    for i in range(n):
        print(color+c2p),
        sys.stdout.softspace=0
    print(c.END)
