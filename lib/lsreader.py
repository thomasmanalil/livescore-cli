def details_reader(details):
    '''
    method to read the match details and return in dictionary format
    the properties included in returned dictionary are:
        time
        score
        home_detail
        away_detail
    #NOTE: Currently the method ignores first and last 3 rows because they contain
           table header and footer and not the match detail itself.
           I'd recommend passing only the match details and not the header and
           footer, and removing the below line. 
    '''
    details = details[1:len(details) - 4]

    def get_goal(goal_detail):
        details_dict = {}
        if u' (pen.) ' in goal_detail[0]:
            goal_detail[0][0] = goal_detail[0][0] + goal_detail[0][2]
        details_dict['goal'] = goal_detail[0][0]
        details_dict['assist'] = goal_detail[1].strip(' (assist) ')
        return details_dict
    
    def get_home_details(home_details):
        details_dict = {}
        if isinstance(home_details[0], list):
            details_dict.update(get_goal(home_details))
        elif u' (pen.) ' in home_details:
            home_details.remove(u' (pen.) ')
            home_details.remove(u'goal')
            details_dict['goal'] = home_details[0] + ' (pen.)'
        else:
            details_dict[home_details[1]] = home_details[0]
        return details_dict
    
    def get_away_details(away_details):
        details_dict = {}
        if isinstance(away_details[0], list):
            away_details[0][0], away_details[0][1] = away_details[0][1], away_details[0][0]
            details_dict.update(get_goal(away_details))
        elif u' (pen.) ' in away_details:
            away_details.remove(u' (pen.) ')
            away_details.remove(u'goal')
            details_dict['goal'] = away_details[0] + ' (pen.)'
        else:
            details_dict[away_details[0]] = away_details[1]
        return details_dict

    def read_row(row):
        details_dict = {}
        i = 0
        details_dict['time'] = row[i]
        i += 1
        if isinstance(row[i], list):
            details_dict['home_detail'] = get_home_details(row[i])
            i += 1
        if not row[i] == u' \xa0 ':
            details_dict['score'] = row[i]
        i += 1
        if len(row) > i:
            details_dict['away_detail'] = get_away_details(row[i])
        return details_dict
    return map(read_row, details)

'''
Pass the dictionary of details to the function to find the max length of each
detail
the returned dict contains the following keys:
    home_goal
    away_goal
    home_stat
    away_stat
'''
def length_finder(details):

    def update_max(dictionary, key, value):
        if dictionary[key] < value:
            dictionary[key] = value
                
    def find_scorer_assister_length(detail):
        if 'goal' in detail:
            scorer_length = len(detail['goal'])
            assister_length = len(detail['assist']) if 'assist' in detail else 0
            total_length = scorer_length + assister_length
        else:
            total_length = 0
        return total_length

    def update_length(details_dict, detail, party):
        if 'goal' in detail:
            update_max(details_dict, party+'_goal', find_scorer_assister_length(detail))
        else:
            for stat in detail:
                update_max(details_dict, party+'_stat', len(stat)+len(detail[stat]))
                
    details_dict = {'home_goal': 0, 'home_stat':0, 'away_goal':0, 'away_stat':0}
    for detail in details:
        if 'home_detail' in detail:
            update_length(details_dict, detail['home_detail'], 'home')
        if 'away_detail' in detail:
            update_length(details_dict, detail['away_detail'], 'away')
    return details_dict



details1 = [[u'match details :', u'show assists'], [u" 4' ", [[u'Florin Andone', u'goal'], u' Guilherme (assist) '], u' 1 - 0 '], [u" 25' ", [u'Fernando Navarro', u'yellowcard'], u' \xa0 '], [u" 28' ", [[u'Florin Andone', u'goal'], u' Emre Colak (assist) '], u' 2 - 0 '], [u" 38' ", u' \xa0 ', [u'yellowcard', u'Roque Mesa']], [u" 39' ", [u'Carles Gil', u'goal'], u' 3 - 0 '], [u" 44' ", [u'Carles Gil', u'yellowcard'], u' \xa0 '], [u" 48' ", [u'Pedro Mosquera', u'yellowcard'], u' \xa0 '], [u" 51' ", u' \xa0 ', [u'yellowcard', u'Hernan Santana']], [u" 54' ", [u'Emre Colak', u'yellowcard'], u' \xa0 ', [u'yellowcard', u'Momo']], [u" 79' ", u' \xa0 ', [u'redyellowcard', u'Hernan Santana']], [u'venue :', u'spectators :'], [u'Estadio Municipal de Riazor', u'21764'], u'referee :', u'Mario Melero (Spain)']
details2 = [[u'match details :', u'show assists'], [u" 6' ", u' 0 - 1 ', [[u'goal', u'Zinedine Machach'], u' (assist) Andy Delort ']], [u" 25' ", u' \xa0 ', [u'yellowcard', u'Ibrahim Sangare']], [u" 28' ", [[u'Jemerson', u'goal'], u' Joao Moutinho (assist) '], u' 1 - 1 '], [u" 30' ", u' \xa0 ', [u'yellowcard', u'Zinedine Machach']], [u" 49' ", [u'Joao Moutinho', u'yellowcard'], u' \xa0 '], [u" 53' ", u' 1 - 2 ', [[u'goal', u'Andy Delort'], u' (assist) Jimmy Durmaz ']], [u" 58' ", [[u'Radamel Falcao', u'goal'], u' Jorge (assist) '], u' 2 - 2 '], [u" 70' ", [[u'Kamil Glik', u'goal'], u' Joao Moutinho (assist) '], u' 3 - 2 '], [u" 81' ", u' \xa0 ', [u'yellowcard', u'Francois Moubandje']], [u'venue :', u'spectators :'], [u'Stade Louis II, Monaco', u'13572'], u'referee :', u'Clement Turpin (France)']
details3 = [[u'match details :', u'show assists'], [u" 14' ", [[u'Nolan Roux', u'goal'], u' Renaud Cohade (assist) '], u' 1 - 0 '], [u" 39' ", [u'Milan Bisevac', u'yellowcard'], u' \xa0 '], [u" 39' ", u' 1 - 1 ', [u'goal', u' (pen.) ', u'Jimmy Briand']], [u" 41' ", u' \xa0 ', [u'yellowcard', u'Lebogang Phiri']], [u" 45' ", u' \xa0 ', [u'yellowcard', u'Yannis Salibur']], [u" 71' ", u' 1 - 2 ', [[u'goal', u'Ludovic Blas'], u' (assist) Pedro Rebocho ']], [u" 85' ", u' 1 - 3 ', [[u'goal', u'Mustapha Diallo'], u' (assist) Ludovic Blas ']], [u'venue :', u'spectators :'], [u'Stade Saint Symphorien', u'14595'], u'referee :', u'Jerome Miguelgorry (France)']
details4 = [[u'match details :', u'show assists'], [u" 2' ", [[u'Alexandre Lacazette', u'goal'], u' Mohamed Elneny (assist) '], u' 1 - 0 '], [u" 5' ", u' 1 - 1 ', [[u'goal', u'Shinji Okazaki'], u' (assist) Harry Maguire ']], [u" 29' ", u' 1 - 2 ', [[u'goal', u'Jamie Vardy'], u' (assist) Marc Albrighton ']], [u" 45' ", [[u'Danny Welbeck', u'goal'], u' Sead Kolasinac (assist) '], u' 2 - 2 '], [u" 56' ", u' 2 - 3 ', [[u'goal', u'Jamie Vardy'], u' (assist) Riyad Mahrez ']], [u" 83' ", [[u'Aaron Ramsey', u'goal'], u' Granit Xhaka (assist) '], u' 3 - 3 '], [u" 85' ", [[u'Olivier Giroud', u'goal'], u' Granit Xhaka (assist) '], u' 4 - 3 '], [u" 90' ", u' \xa0 ', [u'yellowcard', u'Wes Morgan']], [u'venue :', u'spectators :'], [u'Emirates Stadium', u'59387'], u'referee :', u'Mike Dean (England)']
details5 = [[u'match details :', u'show assists'], [u" 29' ", u' \xa0 ', [u'yellowcard', u'Gabriel Jesus']], [u" 70' ", u' 0 - 1 ', [[u'goal', u'Sergio Aguero'], u' (assist) David Silva ']], [u" 75' ", u' 0 - 2 ', [u'goal', u' (o.g.) ', u'Lewis Dunk']], [u" 82' ", u' \xa0 ', [u'yellowcard', u'Raheem Sterling']], [u'venue :', u'spectators :'], [u'The American Express Community Stadium', u'30415'], u'referee :', u'Michael Oliver (England)']
details6 = [[u'match details :', u'show assists'], [u" 9' ", u' \xa0 ', [u'yellowcard', u'Idrissa Gana Gueye']], [u" 27' ", [[u'Cesc Fabregas', u'goal'], u' Alvaro Morata (assist) '], u' 1 - 0 '], u'referee :', u'Jon Moss (England)']

if __name__=='__main__':
    #print(length_finder(details_reader(details1)))
    #print(length_finder(details_reader(details2)))
    #print(length_finder(details_reader(details3)))
    #print(details_reader(details4))

    #print(details_reader(details5))
    print(details6)
    print(details_reader(details6))
