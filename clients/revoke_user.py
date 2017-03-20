import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
import datetime


if not (len(sys.argv)==3):
    print("usage: revoke_user.py <host name> <existing username>")
    quit()

# Put user info into dict
user = dict()
user['username'] = sys.argv[2]
user['timestamp'] = datetime.datetime.utcnow().isoformat()

# Bundle request info
req = dict()
req['arguments'] = json.dumps(user)
req['signature'] = ""
user_rev = urlencode(req)

req = Request(sys.argv[1] + "revoke_user", user_rev.encode('ascii'), method='POST')
query = urlopen(req)

result = json.loads(query.read().decode('ascii'))
print(result['result'])

