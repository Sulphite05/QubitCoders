import requests

username = "sulphite"
r = requests.get(f'https://leetcodeapi-v1.vercel.app/contest/{username}')
print(r.json())