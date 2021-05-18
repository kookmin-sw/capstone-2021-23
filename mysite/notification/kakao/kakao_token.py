import requests
import json

url = "https://kauth.kakao.com/oauth/token"

data = {
    "grant_type" : "authorization_code",
    "client_id" : "{API KEY}",
    "redirect_uri" : "https://localhost.com",
    "code"         : "hW9GZSGwE5B7a0WgrNBd6sg9tPrLOvBsVGedPdCib5aLWsjYKNbPlx5OZubqt-KxtuAdKgorDR4AAAF5Ru2lNg"
    
}
response = requests.post(url, data=data)

tokens = response.json()

print(tokens)

with open("kakao_token.json", "w") as fp:
    json.dump(tokens, fp)
