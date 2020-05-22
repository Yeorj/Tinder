# API Documentation

Forked off of [@FBessez](https://github.com/fbessez/Tinder)'s work.
The Tinder API was initially posted by [@rtt](https://gist.github.com/rtt/10403467#file-tinder-api-documentation-md) who found most of the endpoints.
Since then, more endpoints have been found by [SeanLF](https://github.com/SeanLF) and are stored in a [JSON file](./tinder_api/api_endpoints.json).

## Host and Protocol

| Host | Protocol |
|--|--|
| api.gotinder.com | SSL |

## Required Headers

| Header | Example | Notes |
|---|---|---|
| X-Auth-Token | See "How to get facebook_token" below |  |
| Content-type | application/json |  |
| User-agent | Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00) |  |

## Known Endpoints

Note: All endpoints are concatenated to the host url

Note: All curls must be sent with the headers as well (the only exception is that the /auth call must not have the X-Auth-Token header)

[@SeanLF](https://github.com/SeanLF) found some API endpoints from Tinder's [main.js](https://tinder.com/static/build/chunks/main-04c2dfb832c46d4a6eec.js) file on the Tinder web app and included them in [api_endpoints.json](./tinder_api/api_endpoints.json).

| Endpoint| Purpose| Data?| Method |
|--|--|--|--|
| /auth| For authenticating| {'facebook_token': INSERT_HERE, 'facebook_id': INSERT_HERE}| POST|
| /v2/auth/sms/send?auth_type=sms| Part 1 of SMS authentication (two-factor)| {'phone_number': string}| POST|
| /v2/auth/sms/validate?auth_type=sms| Part 2 of SMS authentication (two-factor)| {'otp_code': string, 'phone_number': string }| POST|
| /v2/auth/login/sms| Part 3 of SMS authentication (two-factor)| {'refresh_token': string}| POST|
| /user/recs| Get match recommendations| {}| GET|
| /v2/matches| Get your matches| query in link should have count=1-100 e.g: /v2/matches?count=50| GET|
| /user/matches/_id| Send Message to that id| {"message": TEXT GOES HERE}| POST|
| /user/matches/match_id| Unmatch person| {}| DELETE |
| /user/_id| Get a user's profile data| {}| GET|
| /user/ping| Change your location| {"lat": lat, "lon": lon}| POST|
| /updates| Get all updates since the given date -- inserting "" will give you all updates since creating a Tinder account (i.e. matches, messages sent, etc.) | {"last_activity_date": ""} Input a timestamp: '2017-03-25T20:58:00.404Z' for updates since that time.| POST|
| /profile| Get your own profile data| {}| GET|
| /profile| Change your search preferences| {"age_filter_min": age_filter_min, "gender_filter": gender_filter, "gender": gender, "age_filter_max": age_filter_max, "distance_filter": distance_filter} | POST|
| /profile| (Tinder Plus Only) hide/show age| {"hide_age":boolean}| POST|
| /profile| (Tinder Plus Only) hide/show distance| {"hide_distance":boolean}| POST|
| /profile| (Tinder Plus Only) hide/show ads| {"hide_ads":boolean}| POST|
| /profile| (Tinder Plus Only) Set Tinder Blend options to "Recent Activity": Shows more recently active users| {"blend":"recency"}| POST|
| /profile| (Tinder Plus Only) Set Tinder Blend options to "Optimal": Scientifically proven to get you more matches| {"blend":"optimal"}| POST|
| /profile| (Tinder Plus Only) Set discovery settings to only people who already liked you| {"discoverable_party":"liked"}| POST|
| /passport/user/travel| (Tinder Plus Only) Travel to coordinate| {"lat":lat,"lon":lon}| POST|
| /v1/activity/feed?direction=past&eventTypes=1023 | Get activity feed, including old and updated bios for comparison| {}| GET|
| /instagram/authorize| Auth Instagram| {}| GET|
| /v2/profile/spotify/| Get Spotify settings| {}| GET|
| /v2/profile/spotify/theme| Set Spotify song| {"id":song_id}| PUT|
| /profile/username| Change your webprofile username| {"username": username}| PUT|
| /profile/username| Reset your webprofile username| {}| DELETE |
| /meta| Get your own meta data (swipes left, people seen, etc..)| {}| GET|
| /v2/meta| Get your own meta data from V2 API (extra data like "top_picks" info)| {}| GET|
| /report/_id| Report someone --> There are only a few accepted causes... (see tinder_api.py for options)| {"cause": cause, "text": explanation}| POST|
| /like/_id| Like someone a.k.a swipe right| {}| GET|
| /pass/_id| Pass on someone a.k.a swipe left| {}| GET|
| /like/_id/super| ~Super Like~ someone a.k.a swipe up| {}| POST|
| /matches/{match id}| Get a match from its id (thanks [@jtabet](https://github.com/jtabet) )| {}| GET|
| /message/{message id}| Get a message from its id (thanks [@jtabet](https://github.com/jtabet) )| {}| GET|
| /passport/user/reset| Reset your location to your real location| {}| POST|
| /passport/user/travel| Change your swiping location| {"lat": latitutde, "lon": longitude}| POST|
| /user/{user_id}/common_connections| Get common connection of a user| {}| GET|
| /profile/job| Set job| {"company":{"id":"17767109610","name":"University of Miami","displayed":true},"title":{"id":"106123522751852","name":"Research Assistant","displayed":true}}| PUT|
| /profile/job| Delete job| {}| DELETE |
| /profile/school| Set school(s)| {"schools":[{"id":school_id}]}| PUT|
| /profile/school| Reset school| {}| DELETE |
| /message/{message_id}/like| Like a message| {}| POST|
| /v2/fast-match/teasers| Get the non blurred thumbnail image shown in the messages-window (the one showing the likes you received)| {}| GET|
| /v2/fast-match/count| Get the number of likes you received| {}| GET|
| /giphy/trending?limit={limit}| Get the trending gifs (tinder uses giphy) accessible in chat| {}| GET|
| /giphy/search?limit={limit}&query={query}| Get gifs (tinder uses giphy) based on a search accessible in chat| {}| GET|

## Status Codes

|Status Code|Explanation|
|--|--|
|200|Everything went okay, and returned a result (if any).|
|301|The server is redirecting you to a different endpoint. This can happen when a company switches domain names, or an endpoint's name has changed.|
|400|The server thinks you made a bad request. This can happen when you don't send the information the API requires to process your request, among other things.|
|401|The server thinks you're not authenticated. This happens when you don't send the right credentials to access an API.|
|404|The server didn't find the resource you tried to access.|
|503|Back-end server is at capacity.|