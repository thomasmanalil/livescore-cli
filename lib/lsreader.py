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

details1 = [[u'match details :', u'show assists'], [u" 4' ", [[u'Florin Andone', u'goal'], u' Guilherme (assist) '], u' 1 - 0 '], [u" 25' ", [u'Fernando Navarro', u'yellowcard'], u' \xa0 '], [u" 28' ", [[u'Florin Andone', u'goal'], u' Emre Colak (assist) '], u' 2 - 0 '], [u" 38' ", u' \xa0 ', [u'yellowcard', u'Roque Mesa']], [u" 39' ", [u'Carles Gil', u'goal'], u' 3 - 0 '], [u" 44' ", [u'Carles Gil', u'yellowcard'], u' \xa0 '], [u" 48' ", [u'Pedro Mosquera', u'yellowcard'], u' \xa0 '], [u" 51' ", u' \xa0 ', [u'yellowcard', u'Hernan Santana']], [u" 54' ", [u'Emre Colak', u'yellowcard'], u' \xa0 ', [u'yellowcard', u'Momo']], [u" 79' ", u' \xa0 ', [u'redyellowcard', u'Hernan Santana']], [u'venue :', u'spectators :'], [u'Estadio Municipal de Riazor', u'21764'], u'referee :', u'Mario Melero (Spain)']
details2 = [[u'match details :', u'show assists'], [u" 6' ", u' 0 - 1 ', [[u'goal', u'Zinedine Machach'], u' (assist) Andy Delort ']], [u" 25' ", u' \xa0 ', [u'yellowcard', u'Ibrahim Sangare']], [u" 28' ", [[u'Jemerson', u'goal'], u' Joao Moutinho (assist) '], u' 1 - 1 '], [u" 30' ", u' \xa0 ', [u'yellowcard', u'Zinedine Machach']], [u" 49' ", [u'Joao Moutinho', u'yellowcard'], u' \xa0 '], [u" 53' ", u' 1 - 2 ', [[u'goal', u'Andy Delort'], u' (assist) Jimmy Durmaz ']], [u" 58' ", [[u'Radamel Falcao', u'goal'], u' Jorge (assist) '], u' 2 - 2 '], [u" 70' ", [[u'Kamil Glik', u'goal'], u' Joao Moutinho (assist) '], u' 3 - 2 '], [u" 81' ", u' \xa0 ', [u'yellowcard', u'Francois Moubandje']], [u'venue :', u'spectators :'], [u'Stade Louis II, Monaco', u'13572'], u'referee :', u'Clement Turpin (France)']
details3 = [[u'match details :', u'show assists'], [u" 14' ", [[u'Nolan Roux', u'goal'], u' Renaud Cohade (assist) '], u' 1 - 0 '], [u" 39' ", [u'Milan Bisevac', u'yellowcard'], u' \xa0 '], [u" 39' ", u' 1 - 1 ', [u'goal', u' (pen.) ', u'Jimmy Briand']], [u" 41' ", u' \xa0 ', [u'yellowcard', u'Lebogang Phiri']], [u" 45' ", u' \xa0 ', [u'yellowcard', u'Yannis Salibur']], [u" 71' ", u' 1 - 2 ', [[u'goal', u'Ludovic Blas'], u' (assist) Pedro Rebocho ']], [u" 85' ", u' 1 - 3 ', [[u'goal', u'Mustapha Diallo'], u' (assist) Ludovic Blas ']], [u'venue :', u'spectators :'], [u'Stade Saint Symphorien', u'14595'], u'referee :', u'Jerome Miguelgorry (France)']
if __name__=='__main__':
    print(details_reader(details1))
    print(details_reader(details2))
    print(details_reader(details3))
