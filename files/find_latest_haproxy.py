import urllib3
import json

http = urllib3.PoolManager()

haproxy_ppas = []
url = "https://api.launchpad.net/1.0/~vbernat/ppas"

response = http.request('GET', url)
if response.status != 200:
    raise Exception(f"Request failed with status code {response.status}, response data: {response.data.decode('utf-8')}")

response_data = json.loads(response.data.decode('utf-8'))
for ppa in response_data["entries"]:
    if ppa["name"].startswith("haproxy"):
        haproxy_ppas.append(ppa["name"])

if haproxy_ppas:
    haproxy_ppas.sort(reverse=True)
    haproxy_version_latest = haproxy_ppas[0].split('-')[1]
    print(haproxy_version_latest)
else:
    raise Exception("No HAProxy PPAs found")
