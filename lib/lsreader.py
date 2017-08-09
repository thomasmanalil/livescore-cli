def details_reader(details):
    '''
    method to read the match details and return in dictionary format
    the properties included in returned dictionary are:
        time
        score
        home_detail
        away_detail
    '''
    details = details[:len(details) - 4]

    def get_goal(goal_detail):
        details_dict = {}
        details_dict['goal'] = goal_detail[0][0]
        details_dict['assist'] = goal_detail[1].strip(' (assist) ')
        return details_dict
    
    def get_home_details(home_details):
        details_dict = {}
        if isinstance(home_details[0], list):
            details_dict.update(get_goal(home_details))
        else:
            details_dict[home_details[1]] = home_details[0]
        return details_dict
    
    def get_away_details(away_details):
        details_dict = {}
        if isinstance(away_details[0], list):
            away_details[0], away_details[1] = away_details[1], away_details[0]
            details_dict.update(get_goal(away_details))
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
Example use
details = [[u" 4' ", [[u'Florin Andone', u'goal'], u' Guilherme (assist) '], u' 1 - 0 '], [u" 25' ", [u'Fernando Navarro', u'yellowcard'], u' \xa0 '], [u" 28' ", [[u'Florin Andone', u'goal'], u' Emre Colak (assist) '], u' 2 - 0 '], [u" 38' ", u' \xa0 ', [u'yellowcard', u'Roque Mesa']], [u" 39' ", [u'Carles Gil', u'goal'], u' 3 - 0 '], [u" 44' ", [u'Carles Gil', u'yellowcard'], u' \xa0 '], [u" 48' ", [u'Pedro Mosquera', u'yellowcard'], u' \xa0 '], [u" 51' ", u' \xa0 ', [u'yellowcard', u'Hernan Santana']], [u" 54' ", [u'Emre Colak', u'yellowcard'], u' \xa0 ', [u'yellowcard', u'Momo']], [u" 79' ", u' \xa0 ', [u'redyellowcard', u'Hernan Santana']], [u'venue :', u'spectators :'], [u'Estadio Municipal de Riazor', u'21764'], u'referee :', u'Mario Melero (Spain)']
details_dict = details_reader(details)
'''
