import os
import re
import requests
def isc2me_compatible(version, modloader):
    url = "https://api.modrinth.com/v2/search"
    payload = {
        "query": "Concurrent Chunk Management Engine",
        "facets": f'[["categories:{modloader}"],["versions:{version}"],["project_type:mod"]]'
    }
    token = os.getenv("MD_API")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"{token}"
    }
    response = requests.get(url, params=payload, headers=headers)
    if response.status_code == 200:
        json = response.json()
        
        if json["total_hits"] <= 0:
            return False
        
        if json["total_hits"] >= 1:
            return True

def isgpu_compatible(version, modloader):
    url = "https://api.modrinth.com/v2/search"
    isc2me = isc2me_compatible(version, modloader)
    payload = {
        "query": "C2ME OpenCL Acceleration Module",
        "facets": f'[["categories:{modloader}"],["versions:{version}"],["project_type:mod"]]'
    }
    token = os.getenv("MD_API")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"{token}"
    }
    response = requests.get(url, params=payload, headers=headers)
    if response.status_code == 200:
        json = response.json()
        
        if json["total_hits"] <= 0 and isc2me:
            return False
        
        if json["total_hits"] >= 1 and isc2me:
            return True

def get_curseforge_modpack_info(curseforge_url):
    pattern = r"([^/]+)$"
    url = "https://api.curseforge.com/v1/mods/search"
    payload = {'gameId': '432', 'slug': re.search(pattern, curseforge_url)}
    token = os.getenv("CF_API")
    headers = {
        "Content-Type": "application/json",
        "x-api-key": f"{token}"
    }
    response = requests.get(url, params=payload, headers=headers)
    if response.status_code == 200:
        return {"successful": True, "response": response.json()}
    
    return {"succesful": False, "response":  "Modpack Not Found"}

def get_modpack_version(curseforge_url):
    json = get_curseforge_modpack_info(curseforge_url)
    if json["successful"]:
        return json["response"]["data"][0]["latestFiles"][0]["gameVersions"][0]
    else:
        return False

def get_modpack_name(curseforge_url):
    json = get_curseforge_modpack_info(curseforge_url)
    if json["successful"]:
        return json["response"]["data"][0]["name"]
    else:
        return False
    
def get_java_version(version, curseforge_url=None):
    url = "https://api.curseforge.com/v1/minecraft/version"
    if curseforge_url:
        version = get_modpack_version(curseforge_url)
    token = os.getenv("CF_API")
    headers = {
        "Content-Type": "application/json",
        "x-api-key": f"{token}"
    }
    print(f"{url}/{version}")
    response = requests.get(f"{url}/{version}", headers=headers)
    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        data = None
        print("Version not found")

    json = requests.get(data["data"]["jsonDownloadUrl"]).json()
    return f"java{json["javaVersion"]["majorVersion"]}"
