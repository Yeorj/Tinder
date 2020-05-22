# coding=utf-8
'''
This file collects important data on your matches,
allows you to sort them by last_activity_date, age,
gender, message count, and their average successRate.
'''

from datetime import date, datetime
from random import random
from time import sleep

def format_matches(matches):
    '''
    Wrap API data to python object for manipulation by helpers.

    :param matches: matches obtained from Tinder API.

    :return: `dict`
        key: person ID
        value: `dict`
            keys: name, match_id, message_count, photos, bio, gender, avg_success_rate, messages, age, distance, last_activity_date
    '''
    formatted_matches = {}
    for match in matches:
        try:
            person = match.get('person')
            person_id = person.get('_id')  # This ID for looking up person
            formatted_matches[person_id] = {
                'match_id': match.get('_id'),  # This ID for messaging
                'message_count': match.get('message_count'),
                'messages': match.get('messages'),
                'last_activity_date': match.get('last_activity_date'),
                'name': person.get('name'),
                'photos': get_photos(person),
                'bio': person.get('bio'),
                'gender': person.get('gender'),
                'age': calculate_age(match.get('person').get('birth_date')),
            }
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            return {'error': message, 'exception': ex}
    return formatted_matches


def get_match_id_by_name(formatted_matches, name):
    '''
    Returns a list of IDs that have the same requested name.

    :param formatted_matches: value from calling :method: `format_matches`.

    :param name: whose name to look for.

    :return: list of IDs that have the same requested name.
    '''
    list_of_ids = []
    for match in formatted_matches:
        if formatted_matches[match]['name'] == name:
            list_of_ids.append(formatted_matches[match]['match_id'])
    if len(list_of_ids) > 0:
        return list_of_ids
    return {'error': "No matches by name of %s" % name}


def get_photos(person):
    '''
    Get a person's photos.

    :param person: whose photos to get.

    :return: list of photo urls.
    '''
    return [photo.get('url', '') for photo in person.get('photos', {})]


def calculate_age(birth_date_string):
    '''
    Converts birthday string to age.

    :param birth_date_string: string from person profile.
        ex: '1997-03-25T22:49:41.151Z'
    
    :return: age.
    '''
    birth_year = int(birth_date_string[:4])
    birth_month = int(birth_date_string[5:7])
    birth_day = int(birth_date_string[8:10])
    today = date.today()
    return today.year - birth_year - ((today.month, today.day) < (birth_month, birth_day))


def distance_in_km(distance_mi):
    '''
    Converts miles into km

    :param distance_mi: distance in miles (int)
    
    :return: distance in km (int)
    '''
    ONE_MILE_IN_KM = 1.60934
    return round(ONE_MILE_IN_KM*distance_mi)


def sort_by_value(formatted_matches, sort_type):
    '''
    Sorts matches by the type requested.

    :param formatted_matches: value from calling :method: `format_matches`.

    :param sort_type: the field to sort by. Possible values:
        name, match_id, message_count, bio, gender, messages, age, last_activity_date
    '''
    return sorted(formatted_matches.items(), key=lambda x: x[1][sort_type], reverse=True)


def how_long_in_words(duration, include_seconds=False):
    '''
    Converts a datetime difference into words.

    :param duration: datetime difference.

    :param include_seconds: whether to include seconds or not.

    :return: duration in words.
    '''
    secs = duration.seconds
    days = duration.days
    m, s = divmod(secs, 60)
    h, m = divmod(m, 60)
    how_long = ("%d days, %d hrs %02d min" % (days, h, m))
    if include_seconds:
        how_long = ("%s %02d s" % (how_long, s))
    return how_long


def how_long_in_words_since(ping_time):
    '''
    How long since a person was seen on Tinder.

    :return: duration formatted as a `string`.
    '''
    ping_time = ping_time[:len(ping_time) - 5]
    datetime_ping = datetime.strptime(ping_time, '%Y-%m-%dT%H:%M:%S')
    return how_long_in_words(datetime.utcnow() - datetime_ping)


def how_long_since_last_seen(match):
    '''
    How long since a match was last interacted with on Tinder.

    :return: duration formatted as a `string`.
    '''
    return how_long_in_words_since(match['last_activity_date'])


def how_long_since_last_seen_all(formatted_matches):
    '''
    How long since each matched person was last interacted with on Tinder.

    :param formatted_matches: value from calling :method: `format_matches`.

    :return: :class: `dict` like `{match_id: {'person': {'id': id, 'name': name}, 'duration': duration}}`
    '''
    return {
        match['_id']: {
            'person': {
                'id': match['person']['id'],
                'name': match['person']['name']
            },
            'duration': how_long_since_last_seen(match)
        }
    for match in formatted_matches }


def pause():
    '''
    In order to appear as a real Tinder user using the app...
    When making many API calls, it is important to pause a...
    realistic amount of time between actions to not make Tinder...
    suspicious!
    '''
    pause_duration = 3 * random()
    sleep(pause_duration)