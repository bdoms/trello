Copyright &copy; 2015, [Brendan Doms](http://www.bdoms.com/)  
Licensed under the [MIT license](http://www.opensource.org/licenses/MIT)  


# Trello

A Python interface to the Trello API.


## Existing Solutions

There are a lot of other Python libraries out there to work with the Trello API,
but I've found that pretty much all of them have one of these two issues:

 * __They simply don't work.__ Several of the frameworks I tried just failed mysteriously.
These projects might not have adapted to changes by Trello, or maybe they based their calls entirely on the docs
instead of actually trying them in real life. The docs themselves are confusing, and sometimes flat out wrong themselves,
which means that if you don't actually try a request even though the docs say it should work, it still might not.
 * __They rely on third-party libraries.__ The Trello API is a simple REST API that returns JSON.
Authentication is adding two parameters. There's really no reason to need anything
beyond a few lines of the Python standard library to make those requests and parse the responses.


## Setup

You need to gather a few variables in order to properly interact with the API.

### `api_key`

This is found on [the Trello website](https://trello.com/app-key)

### `board_name` and `board_id`

The name and ID for the board you want to access are found in the board URL, which is formatted like:

```
https://trello.com/b/[BOARD_ID]/[BOARD_NAME]
```

### `oauth_token`

Now that you have the required info you need to generate a token
by going to a URL in your browser that includes your `api_key` and `board_name`:

```
https://trello.com/1/authorize?response_type=token&scope=read,write&expiration=never&key=[API_KEY]&name=[BOARD_NAME]
```

### `list_id`

It is surprisingly hard to find a list's ID via the Trello interface,
but easy to get via the API, so I built a helper function.
To get the ID, simply call the provided `trello.py` file from the command line with the following arguments:

```bash
python __init__.py api_key oauth_token board_id list_name
```

Note that `list_name` is the case sensitive display name at the top of the list.
