from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from . import config # import the config variables in the file './config.py'.

public_key_file = open('public.pem', 'r')
public_key = public_key_file.read()

def user(request, username):
    user_json = {"@context": "https://www.w3.org/ns/activitystreams",
        "id": config.site_url + "/users/" + username,
        "inbox": config.site_url +  "/users/" + username + "/inbox",
        "outbox": config.site_url + "/users/" + username + "/outbox",
        "type": "Person", # the json for the type
        "name": username , # user name
        "preferredUsername": username,
        "publicKey": {
            "id": config.site_url + "/users/" + username + "#main-key",
            "owner": config.site_url + "/users/" + username,
            "publicKeyPem": public_key
        }
    } 

    if username != 'john':
        raise Http404() # throw 404
    else:
        # return json file with setting content_type
       return HttpResponse(json.dumps(user_json), content_type="application/activity+json")

# send webfinger info
def webfinger(request):
    webfinger = request.GET.get('resource')

    user_name = "john"
    account = "acct:" + user_name + "@" + config.site_domain_name


    if webfinger != account:
        raise Http404()

    webfinger_json = {
        "subject": account, # acct:john@example.net
        "links": [
            {
                "rel": "self",
                "type": "application/activity+json",
                "href": config.site_url + "/users/" + user_name
            }
        ]
    }

    return HttpResponse(json.dumps(webfinger_json), content_type = "application/activity+json")

# inbox only accept post
@csrf_exempt # naccessary
def inbox(request, username):
    log = open('log.txt', 'a') # store the inbox messages
    
    if username != 'john':
        raise Http404()
    
    else:
        header = request.headers
        data = request.body

        text = f'\nmail: {header} \n{data}\n'

        print(text)

        log.write(text)

        log.close()

        return HttpResponse("OK", status="202")
