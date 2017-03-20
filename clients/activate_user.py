import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
import datetime

if not (len(sys.argv)==5):
    print("usage: activate_user.py <host name> <new username> <password> <role:facofc or logofc>")
    quit()

# Put user info into dict
user = dict()
user['username'] = sys.argv[2]
user['password'] = sys.argv[3]
user['role'] = sys.argv[4]
user['timestamp'] = datetime.datetime.utcnow().isoformat()

# Bundle request info
req = dict()
req['arguments'] = json.dumps(user)
req['signature'] = ""
user_req = urlencode(req)

req = Request(sys.argv[1] + "activate_user", user_req.encode('ascii'), method='POST')
query = urlopen(req)

result = json.loads(query.read().decode('ascii'))
print(result['result'])

