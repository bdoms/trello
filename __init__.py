import json
from urllib import urlencode
from urllib2 import HTTPError, Request, urlopen
import sys


# API example: https://github.com/sarumont/py-trello/blob/master/trello/__init__.py
class Trello(object):

    def __init__(self, api_key, oauth_token, board_id):
        self.api_key = api_key
        self.oauth_token = oauth_token
        self.board_id = board_id
        self.base_url = 'https://api.trello.com/1'

    def getLists(self):
        return self.makeRequest('GET', '/boards/' + self.board_id + '/lists')

    def getList(self, list_id):
        return self.makeRequest('GET', '/lists/' + list_id)

    def findList(self, name):
        tlist = None
        lists = self.getLists()
        for l in lists:
            if l['name'] == name:
                tlist = l
                break
        return tlist

    def createList(self, name, list_id):
        new_list = self.findList(name)
        if not new_list:
            # NOTE that because of Trello's weird positioning mechanics
            #      this may not always put the new list just to the right of the old one, but it'll be close
            done_list = self.getList(list_id)
            params = {'name': name, 'pos': done_list['pos'] + 1}
            new_list = self.makeRequest('POST', '/boards/' + self.board_id + '/lists', params=params)
        return new_list

    def getCard(self, card_number):
        return self.makeRequest('GET', '/boards/' + self.board_id + '/cards/' + card_number)

    def addComment(self, card, comment):
        params = {'text': comment}
        return self.makeRequest('POST', '/cards/' + card['id'] + '/actions/comments', params=params)

    def getCards(self, list_id):
        return self.makeRequest('GET', '/lists/' + list_id + '/cards')

    def moveCard(self, card, list_id, pos=None):
        params = {'idList': list_id}
        if pos:
            params['pos'] = pos
        self.makeRequest('PUT', '/cards/' + card['id'], params=params)

    def moveCards(self, from_list_id, to_list_id):
        cards = self.getCards(from_list_id)
        for card in cards:
            self.moveCard(card, to_list_id, pos=card['pos'])

    def makeRequest(self, method, path, params=None):
        if not params:
            params = {}
        params['key'] = self.api_key
        params['token'] = self.oauth_token
        
        url = self.base_url + path
        data = None

        if method == 'GET':
            url += '?' + urlencode(params)
        elif method in ['POST', 'PUT']:
            data = urlencode(params)

        request = Request(url)
        if method == 'PUT':
            request.get_method = lambda: method

        try:
            if data:
                response = urlopen(request, data=data)
            else:
                response = urlopen(request)
        except HTTPError as e:
            print e
            print e.read()
            result = None
        else:
            result = json.loads(response.read())

        return result


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print 'Wrong number of arguments. Need api_key, oauth_token, board_id and list_name.'
        sys.exit()
    filename, api_key, oauth_token, board_id, list_name = sys.argv
    client = Trello(api_key, oauth_token, board_id)
    tlist = client.findList(list_name)
    if tlist:
        print 'List ID: ' + tlist['id']
    else:
        print 'List not found.'
