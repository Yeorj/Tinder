# coding=utf-8
'''
Tinder API python wrapper
~~~~~~~~~~~~~~~~~~~~~~~~~

Read `readme.md` and `Tinder API.ipnyb` for usage.

:license: MIT, see LICENSE for more details.
'''

import json
import requests
from tinder_api.api_endpoints import API_ENDPOINTS

class Tinder_API(object):
    def __init__(self, host= 'https://api.gotinder.com', headers={}, api_token=None):
        self._host = host
        self._not_authenticated_error = {'error': 'Please authenticate first.'}
        self._API_ENDPOINTS = API_ENDPOINTS
        self._headers = headers if headers != {} else {
            'app_version': '11.15.0',
            'platform': 'ios',
            'User-agent': 'Tinder/11.15.0 (iPhone; iOS 15.5.0; Scale/2.00)',
            'Accept': 'application/json',
            'content-type': 'application/json',
        }
        self._auth_key = 'X-Auth-Token'
        self._content_type = 'content-type'
        if api_token is not None:
            self.authenticate(api_token)


    # AUTHENTICATION METHODS

    def authenticate(self, api_token):
        '''
        Sets the authenticate header attribute.
        '''
        self._headers.update({self._auth_key: api_token})


    # SMS authentication

    def send_otp_code(self, phone_number):
        '''
        Request a one time password from Tinder via SMS.

        :param phone_number: the phone number to send the otp to.
        '''
        return self.api_request('auth', 'smsSend', data={'phone_number': phone_number})


    def get_refresh_token(self, phone_number, otp_code):
        '''
        Gets the refresh token.

        :param phone_number: the user's phone number.

        :param otp_code: received by the user on the number provided.
        '''
        response_body = self.api_request('auth', 'smsValidate', data={'otp_code': otp_code, 'phone_number': phone_number})
        return response_body.get("data", {}).get("refresh_token")


    def get_api_token(self, refresh_token):
        '''
        Gets the API token from the refresh token. Will also authenticate.

        :param refresh_token: Refresh token obtained from :method:`get_refresh_token`.
        '''
        data = {'refresh_token': refresh_token }
        response_body = self.custom_request(self._API_ENDPOINTS['authApiPath'] + '/sms', http_verb='POST', data=data)
        api_token = response_body.get("data", {}).get("api_token", None)
        self.authenticate(api_token)
        return api_token


    # FB authentication

    def get_facebook_auth_token(self, facebook_auth_token, facebook_user_id):
        '''
        Get api_token using Facebook.

        :param facebook_auth_token: the Facebook auth token of the user to authenticate.

        :param facebook_user_id: the Facebook ID of the user to authenticate.
        '''
        response_body = self.custom_request('/auth', http_verb='POST', data={'facebook_token': facebook_auth_token, 'facebook_id': facebook_user_id})
        token = response_body['token']
        self.authenticate(token)
        return token


    # APP FUNCTIONALITY

    def get_recommendations(self):
        '''
        Returns a list of users that you can swipe on.
        '''
        return self.custom_request('/user/recs')


    def get_recs_v2(self):
        '''
        This works more consistently then the normal get_recommendations becuase it seeems to check new location.
        '''
        return self.api_request('recs', 'getRecs')


    def get_updates(self, last_activity_date=None):
        '''
        Returns all updates since the given activity date.

        :param last_activity_date: The last activity date is defaulted at the beginning of time.
            Format: '2017-07-09T10:28:13.392Z'
        '''
        return self.api_request('user', 'getUpdates', data={'last_activity_date': last_activity_date})


    def get_self(self):
        '''
        Returns your own profile data
        '''
        return self.custom_request('/profile')


    def get_self_v2(self):
        '''
        Returns your own profile data. Does not seem to work.
        '''
        return self.api_request('profile', 'getUserProfile')


    def change_preferences(self, preferences):
        '''
        Changes your search preferences.

        :param kwargs: a dictionary:
            age_filter_min: 18..46
            age_filter_max: 22..55
            age_filter_min <= age_filter_max - 4
            gender: 0 == seeking males, 1 == seeking females
            distance_filter: 1..100
            discoverable: true | false
            {'photo_optimizer_enabled':false}
        
        example: change_preferences(age_filter_min=30, gender=0)
        '''
        return self.custom_request('/profile', http_verb='POST', data=preferences)


    def get_meta(self):
        '''
        Returns meta data on yourself. Including the following keys:
        ['globals', 'client_resources', 'versions', 'purchases',
        'status', 'groups', 'products', 'rating', 'tutorials',
        'travel', 'notifications', 'user']
        '''
        return self.custom_request('/meta')


    def get_meta_v2(self):
        '''
        Returns meta data on yourself from V2 API. Including the following keys:
        ['account', 'client_resources', 'plus_screen', 'boost',
        'fast_match', 'top_picks', 'paywall', 'merchandising', 'places',
        'typing_indicator', 'profile', 'recs']
        '''
        return self.api_request('meta', 'getMeta')


    def update_location(self, lat, lon):
        '''
        Updates your location to the given float inputs.
        Note: Requires a passport / Tinder Plus.

        :param lat: latitude.

        :param lon: longitude.
        '''
        return self.api_request('passport', 'submitPassportLocation', data={'lat': lat, 'lon': lon})

    def reset_real_location(self):
        '''
        Reset your real location.
        Note: Requires a passport / Tinder Plus.
        '''
        return self.api_request('passport', 'resetPassportLocation')


    def set_webprofileusername(self, username):
        '''
        Sets the username for the webprofile.

        :param username: string
            ex: https://www.gotinder.com/@YOURUSERNAME
        '''
        return self.custom_request('/profile/username', http_verb='PUT', data={'username': username})

    def reset_webprofileusername(self, username):
        '''
        Resets the username for the webprofile

        :param username: ?
        '''
        return self.custom_request('/profile/username', http_verb='DELETE')


    def get_person(self, id):
        '''
        Gets a user's profile via their id

        :param id: ID of the user to find
        '''
        return self.api_request('user', 'getOtherUserById', userId=id)


    def send_msg(self, match_id, msg):
        '''
        Send a message to a match

        :param match_id: match

        :param msg: message to send
        '''
        return self.api_request('user', 'sendMessage', data={'message': msg}, matchId=match_id)


    def unmatch(self, match_id):
        '''
        Unmatch someone

        :param match_id: person to unmatch
        '''
        return self.api_request('user', 'unmatch', matchId=match_id)


    def superlike(self, user_id):
        '''
        Superlike someone

        :param user_id: person to superlike
        '''
        return self.like(user_id, action='superlike')


    def like(self, user_id, action='like'):
        '''
        Like someone

        :param user_id: person to like
        '''
        endpoint = {'superlike': 'recSuperLike', 'like': 'recLike', 'dislike': 'recDislike'}[action]
        return self.api_request('recs', endpoint, userId=user_id)


    def dislike(self, user_id):
        '''
        Dislike someone

        :param user_id: person to dislike
        '''
        return self.like(user_id, action='dislike')


    def report(self, user_id, cause, explanation=''):
        '''
        Report someone
        
        :param cause: There are three options for cause:
            0 : Other and requires an explanation
            1 : Feels like spam and no explanation
            4 : Inappropriate Photos and no explanation

        :param explanation: optional user comment
        '''
        return self.api_request('report', 'reportUser', data={'cause': cause, 'text': explanation}, userId=user_id)


    def get_match(self, match_id):
        '''
        Get info from match

        :param match_id: ID of the match to get info about
        '''
        return self.api_request('user', 'getMatch', matchId=match_id)


    def matches(self, limit=60, page_token=None):
        '''
        Get matches, in increments of roughly 60. Use the page token in the response to obtain the next set.

        :param limit: maximum number of matches to get.

        :param page_token: Page offset. Obtained in this function's response.
        '''
        return self.api_request('user', 'getMatches', data={'count': limit, 'page_token': page_token})


    def fast_match_count(self):
        '''
        Get your match count. Returns a value between 0 and 99.
        '''
        return self.api_request('recs', 'fastMatchCount')

    
    def fast_match_teasers(self):
        '''
        Get the non blurred thumbnail image shown in the messages-window (the one showing the likes you received).
        '''
        return self.api_request('recs', 'fastMatchTeasers')


    def trending_gifs(self, limit=3):
        '''
        Get trending GIFs.

        :param limit: limit to the number of results.
        '''
        return self.api_request('gif', 'trending', data={'limit': limit})


    def gif_query(self, query, limit=3):
        '''
        Search for GIFs.

        :param limit: limit to the number of results.
        '''
        return self.api_request('gif', 'search', data={'limit': limit, 'query': query})


    def api_request(self, service, endpoint, data={}, **kwargs):
        '''
        Perform an API request to the service and endpoint provided, with the data provided.

        :param service: Tinder API service from `api_endpoints.json`.

        :param endpoint: Tinder API service endpoint from `api_endpoints.json`.

        :param data: data to send with the request.

        :return: :class:`requests.Reponse`
        '''
        api_endpoint = self.get_endpoint(service, endpoint)
        return self.custom_request(api_endpoint.get('path').format(**kwargs), http_verb=api_endpoint.get('method', 'GET'), data=data)

    
    def get_endpoint(self, service, endpoint):
        return self._API_ENDPOINTS['services'].get(service)['endpoints'].get(endpoint)


    def custom_request(self, endpoint, http_verb='get', data={}):
        '''
        Allow calling any endpoint of the Tinder API.

        :param endpoint: endpoint (part of the link after host).

        :param data: To be sent with the request. If the http 
        request using the verb specified supports a request body,
        then convert the data to a JSON string, otherwise it is
        converted to a query string.

        :param http_verb: HTTP verb.
            Can be: get, head, post, patch, put, delete, options

        :return: response object
        '''
        if self._auth_key not in self._headers and '/auth' not in endpoint:
            return self._not_authenticated_error
        
        http_verb_functions={ 'get': requests.get, 'head': requests.head, 'post': requests.post, 'patch': requests.patch, 'put': requests.put, 'delete': requests.delete, 'options': requests.options }
        request_has_body={ 'get': False, 'head': False, 'post': True, 'patch': True, 'put': True, 'delete': True, 'options': False }
        response_has_body={ 'get': True, 'head': False, 'post': True, 'patch': True, 'put': False, 'delete': True, 'options': True }
        
        http_verb = http_verb.lower()
        url = self._host + endpoint
        http_verb_function = http_verb_functions[http_verb.lower()]

        if not request_has_body[http_verb]:
            url += self.data_to_query_string(data)
            data = None
        else:
            data = json.dumps(data)

        try:
            # call API and developer must figure out what to do with responses with no body
            response = http_verb_function(url, headers=self._headers, data=data)
            return response.json() if response_has_body[http_verb] else response
        except Exception as e:
            return {'error': 'Something went wrong.', 'exception': str(e)}


    def data_to_query_string(self, data):
        '''
        Converts a dict into a query string

        :param data: data to be included in a query string

        :return: query string
        '''
        if type(data) is dict and data != {}:
            return '?' + '&'.join([f"{key}={value}" for key, value in data.items() if value is not None and value != ''])
        return ''