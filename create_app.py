import requests
from azure.identity import ClientSecretCredential
import urllib.request
import urllib.parse
import json


client_ids = ""
tenant_ids = ""
secrets = ""


def client():
    client_id = client_ids
    tenant_id = tenant_ids
    secret = secrets
    credentials = ClientSecretCredential(
        client_id=client_id,
        client_secret=secret,
        tenant_id=tenant_id
    )
    # Create a Graph client
    #graph_client = GraphClient(credential=credentials)

    access_token = credentials.get_token('https://graph.microsoft.com/.default').token
    #print(access_token)
    g_client = requests.Session()
    g_client.headers.update({'Authorization': 'Bearer ' + access_token})
    return g_client


def hunt_client(hunt_query):
    tenantId = tenant_ids  # Paste your own tenant ID here
    appId = client_ids  # Paste your own app ID here
    appSecret = secrets  # Paste your own app secret here

    url = "https://login.microsoftonline.com/%s/oauth2/token" % (tenantId)

    resourceAppIdUri = 'https://api.securitycenter.microsoft.com'

    body = {
        'resource': resourceAppIdUri,
        'client_id': appId,
        'client_secret': appSecret,
        'grant_type': 'client_credentials'
    }

    data = urllib.parse.urlencode(body).encode("utf-8")

    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)
    jsonResponse = json.loads(response.read())
    aadToken = jsonResponse["access_token"]
    query = hunt_query  # Paste your own query here

    url = "https://api.securitycenter.microsoft.com/api/advancedqueries/run"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': "Bearer " + aadToken
    }

    data = json.dumps({'Query': query}).encode("utf-8")

    req = urllib.request.Request(url, data, headers)
    response = urllib.request.urlopen(req)
    jsonResponse = json.loads(response.read())
    #schema = jsonResponse["Schema"]
    results = jsonResponse["Results"]
    return results