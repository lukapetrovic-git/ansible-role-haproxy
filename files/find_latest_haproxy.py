import urllib3
import json
from urllib.parse import urljoin
from argparse import ArgumentParser

arguments = ArgumentParser()
arguments.add_argument(
    "--ubuntu-release-name",
    dest="ubuntu_release_name",
    type=str,
    help="Ubuntu release name, e.g. 'noble'",
    required=True,
)
arguments.add_argument(
    "--ubuntu-architecture",
    dest="ubuntu_architecture",
    type=str,
    help="Ubuntu architecture, e.g. 'amd64'",
    required=True,
)
arguments = arguments.parse_args()

http = urllib3.PoolManager()

haproxy_ppas = []
url = "https://api.launchpad.net/1.0/~vbernat/ppas"

response = http.request('GET', url)
if response.status != 200:
    raise Exception(
        f"Request failed with status code {response.status}, response data: {response.data.decode('utf-8')}")

response_data = json.loads(response.data.decode('utf-8'))

for ppa in response_data["entries"]:
    if ppa["name"].startswith("haproxy"):
        ppa_binaries_url = urljoin(
            ppa["self_link"], f"?ws.op=getPublishedBinaries&status=Published&distro_arch_series=https://api.launchpad.net/1.0/ubuntu/{arguments.ubuntu_release_name}/{arguments.ubuntu_architecture}")
        ppa_binaries_response = http.request('GET', ppa_binaries_url)
        if ppa_binaries_response.status != 200:
            raise Exception(
                f"Request failed with status code {ppa_binaries_response.status}, response data: {ppa_binaries_response.data.decode('utf-8')}")
        ppa_binaries_data = json.loads(
            ppa_binaries_response.data.decode('utf-8'))
        if ppa_binaries_data["total_size"] > 0:
            haproxy_ppas.append(ppa["name"])

if haproxy_ppas:
    haproxy_ppas.sort(reverse=True)
    haproxy_version_latest = haproxy_ppas[0].split('-')[1].strip()
    print(haproxy_version_latest)
else:
    raise Exception("No HAProxy PPAs found")
