import spacy

nlp = spacy.load('en_core_web_sm')

book_query = ['i want to book a ticket from London to New York on 5/5/2018 after 3.30 pm',
              'book me a ticket to Berlin on 5/5/2018 after 5.30 pm']
cancel_query = ['i would like to cancel my ticket with PNR 1001',
                'cancel my Lufthansa flight ticket from London to New York']
web_check_in = ['i would like to web checkin to my flight with PNR 1002',
              'i want to webcheckin to my Lufthansa flight to New York']


def get_city(text):
    """
    get cities a part of the query
    :param text: string query
    :return: city: list of cities
    """

    doc = nlp(unicode(text))
    city = []
    word = ""
    for index in range(len(doc)):
        if doc[index].pos_ == 'PROPN' and doc[index].ent_type_ == 'GPE':
            if index + 1 < len(doc) and doc[index + 1].pos_ == 'PROPN' and doc[index].ent_type_ == 'GPE':
                word = word + str(doc[index]) + " "
                continue
            else:
                word = word + str(doc[index])
                city.append(word)
                word = ""
    return city


print get_city(book_query[0])


def get_date(text):
    """
    get the dates a part of the query
    :param text: string query
    :return: date: list of dates
    """

    doc = nlp(unicode(text))
    date = []
    word = ""
    for index in range(len(doc)):
        if doc[index].ent_type_ == 'DATE':
            if index + 1 < len(doc) and doc[index + 1].ent_type_ == 'DATE':
                word = word + str(doc[index]) + " "
                continue
            else:
                word = word + str(doc[index])
                date.append(word)
    return None if date == [] else date[0]


print get_date(book_query[0])


def get_time(text):
    """
    get the times specified in the query as a list
    :param text: string query
    :return: time: list of times a part of the query
    """

    doc = nlp(unicode(text))
    time = []
    word = ""
    for index in range(len(doc)):
        if doc[index].ent_type_ == 'TIME':
            if index + 1 < len(doc) and doc[index + 1].ent_type_ == 'TIME':
                word = word + str(doc[index]) + " "
                continue
            else:
                word = word + str(doc[index])
                time.append(word)
    return time


print get_time(book_query[0])


def get_pnr(text):
    """
    get the pnr numbers specified in the query
    :param text: string query
    :return: list of pnr numbers specified
    """

    doc = nlp(unicode(text))
    pnr = []
    for index in range(len(doc)):
        if doc[index].pos_ == 'NUM':
            pnr.append(str(doc[index]))
    return None if pnr == [] else pnr[0]


print get_pnr(web_check_in[0])


def get_airline(text):
    """
    get the name of the airline, if specified in the query
    :param text: string query
    :return: list of airlines specified
    """

    doc = nlp(unicode(text))
    airline = []
    word = ""
    for index in range(len(doc)):
        if doc[index].ent_type_ == 'ORG':
            if index + 1 < len(doc) and doc[index + 1].ent_type_ == 'ORG':
                word = word + str(doc[index]) + " "
                continue
            else:
                word = word + str(doc[index])
                airline.append(word)
    return None if airline == [] else airline[0]


print get_airline(cancel_query[1])


def get_city_of_origin(text):
    """
    return the origin city. generalisation - it is the first city specified in the query.
    :param text: string query
    :return: string origin
    """
    city = get_city(text)
    if len(city) == 0 or len(city) == 1:
        return None
    else:
        return city[0]


print get_city_of_origin(book_query[0])

def get_destination_city(text):
    """
    return destination of flight. generalization - generally specified second, or only specified
    :param text: string query
    :return: destination
    """

    city = get_city(text)
    if not len(city):
        return None
    elif len(city) == 1:
        return city[0]
    else:
        return city[1]


print get_destination_city(book_query[1])
