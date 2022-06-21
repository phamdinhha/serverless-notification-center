import requests
import jwt
import json
import os


def handler(event, context):
    print(event)
    protocol = getWebsocketProtocolHeader(event["headers"])
    if protocol != "websocket":
        raise ValueError("invalid websocket protocol")
    if not event['queryStringParameters'].get("access_token"):
        raise ValueError("missing access token")
    access_token = event['queryStringParameters'].get("access_token")
    print("access token: ", access_token)
    try:
        claims = verifyJwt(access_token)
        print("claims: ", claims)
        print("methodArn: ", event["methodArn"])
        return {
            "principalId": claims["email"],
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [{
                    "Action": "execute-api:Invoke",
                    "Effect": "Allow",
                    "Resource": event["methodArn"]
                }]
            },
            "context": {
                "userId": claims["email"]
            }
        }
    except Exception as e:
        print("Exception: ", e)
        raise Exception("Failed to authentication")

def getWebsocketProtocolHeader(headers):
    for header in headers:
        if header.lower() == 'sec-websocket-protocol':
            return headers[header]
    return None


def verifyJwt(access_token):
    public_key = get_public_key(os.environ["ISSUER"])
    try:
        print("verify token: ")
        claims = jwt.decode(access_token, key=public_key, algorithms=['RS256'], audience='user')
        return claims
    except Exception as e:
        print(e)
        raise(e)


def get_public_key(issuer):
    resp = requests.get(issuer)
    exp_key = resp.json()["data"][0]
    public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(exp_key))
    print("public key: ", public_key)
    return public_key

