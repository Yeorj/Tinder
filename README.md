# Tinder API - 2020

Forked off of [@FBessez](https://github.com/fbessez/Tinder)'s work. This library has been completely refactored, and documented.
The Tinder API was initially posted by [@rtt](https://gist.github.com/rtt/10403467#file-tinder-api-documentation-md) who found most of the endpoints.
Since then, more endpoints have been found by [SeanLF](https://github.com/SeanLF) and are stored in a [JSON file](./tinder_api/api_endpoints.json).

## [API Documentation](./API_Documentation.md) 👈 link

**Note: This was updated in May 2020 so it might be outdated.**

**Note: Using this package violates Tinder's [Terms of Use](https://policies.tinder.com/terms/intl/en).**

## Installation

```bash
pip install git+https://github.com/SeanLF/Tinder
```

You can also add the project as a dependency by adding `git+https://github.com/SeanLF/Tinder` to your pip's `requirements.txt` file.

We plan on publishish this project as a package on PyPI.

## Library documentation

### Tinder_API usage

`api.py` contains a class called Tinder_API that provides a python wrapper for the Tinder API.

#### Optional parameter when instantiating Tinder_API

- `host`: defaults to `https://api.gotinder.com`.
- `api_token`: specify if you have it already.

#### Authenticating with Facebook

Use the `facebook_auth_token.py` module to obtain Facebook credentials. Built with the help of [@PhillipeRemy](https://github.com/philipperemy/Deep-Learning-Tinder/blob/master/tinder_token.py)

```python
from tinder_api import Tinder_API
from tinder_api import facebook_auth_token

# User provides facebook_username & facebook_password.
facebook_auth_token = facebook_auth_token.get_facebook_access_token(facebook_username, facebook_password)
facebook_user_id = facebook_auth_token.get_facebook_id(facebook_access_token)
tinder_api = Tinder_API()
tinder_api.get_facebook_auth_token(facebook_auth_token, facebook_user_id)
# You can now call the API.
```

#### SMS Authentication

As opposed to Facebook auth, there's a rate limit to the number of SMS you can receive in an hour (supposedly 60).
Therefore, it is better to get your token once and use it within its 24 hour lifetime rather than asking for a new one everytime.
(implemented by [@Tagge](https://github.com/Tagge))

```python
from tinder_api import Tinder_API

tinder_api = Tinder_API()
# User provides the phone number.
tinder_api.send_otp_code(phone_number)
# User receives and provides OTP code.
refresh_token = tinder_api.get_refresh_token(phone_number, otp_code)
# Obtain an api_token valid for 24 hours.
api_token = tinder_api.get_api_token(refresh_token)
# You can now call the API.

# When api_token expires, call with the refresh token you have hopefully stored somewhere.
api_token = tinder_api.get_api_token(refresh_token)
# You can now call the API.
```

##### If you already have an API token stored

```python
from tinder_api import Tinder_API

# stored_api_token could be stored in a web session object.
tinder_api = Tinder_API(api_token=stored_api_token)
```

### Helper functions

See the documentation in `helpers.py` for more information, in particular for parameter and return documentation.

```python
def wrap_matches(matches): # Wrap API data to python object for manipulation by helpers.

def get_match_id_by_name(match_info, name): # Returns a list of IDs that have the same requested name.

def get_photos(person): # Get a person's photos.

def calculate_age(birth_date_string): # Converts birthday string to age.

def distance_in_km(distance_mi): # Converts miles into km

def sort_by_value(match_info, sort_type): # Sorts matches by the type requested.

def how_long_in_words(duration, include_seconds=False): # Converts a datetime difference into words.

def how_long_in_words_since(ping_time): # How long has it been since this date in words.

def how_long_since_last_seen(match): # How long has it been since the last interaction with a Tinder match.

def how_long_since_last_seen_all(matches): # How long has it been since the last interaction with each Tinder match.

def pause(): # In order to appear as a real Tinder user using the app...
             # When making many API calls, it is important to pause a...
             # realistic amount of time between actions to not make Tinder...
             # suspicious!
```

### More examples

You may also look at the jupyter notebook (`Tinder API.ipynb`) for more examples. [@GloriaMacia](https://github.com/gloriamacia) and [@FBessez](https://github.com/fbessez/Tinder) have contributed.

The best option would be to look at the [tests](./tests/test.py) file as it sets up both SMS and Facebook authentication, and calls most API endpoints.

### ~~Config File~~

[@SeanLF](https://github.com/SeanLF) has removed the use of the config file after refactoring this library to use the Tinder_API class.

## Maintaining this library

### Set-up

To get started, run:

```bash
python setup.py install
```

This will install the project to your machine, with its dependencies.

Upon installation, the project generates a python file `api_endpoints.py` in the installation folder.
**The project won't be able to make API calls using the standard functions without it!**

### Testing

Please run before pushing changes to ensure that you aren't breaking anything.
**Note: this requires installing the project.**

```bash
python tests/test.py
```
