import requests
from requests.structures import CaseInsensitiveDict
import re


proxies = {"http": "http://127.0.0.1:8081", "https": "http://127.0.0.1:8081"}
def getCookies():
    getCookies.host_session = input("Please paste the value of your __Host-session here: ")
    getX_CSRF_TOKEN()

def getX_CSRF_TOKEN():

    url = "https://hackerone.com//opportunities/all"
    headers = CaseInsensitiveDict()
    headers = {"Cookie": getCookies.host_session}

    response = requests.get(url=url,headers=headers,allow_redirects=False,proxies=proxies, verify=False) 

    response_content = response.text

    match = re.search(r'<meta\s+name=["\']csrf-token["\']\s+content=["\']([^"\']+)["\']\s*/?>', response_content)

    # Check if a match was found
    if match:
        getX_CSRF_TOKEN.x_csrf_token = match.group(1)  # Extract the content attribute value
        print(f"X-CSRF-Token: {getX_CSRF_TOKEN.x_csrf_token}")
    else:
        print("CSRF token not found.")



def main():
    getCookies()


if __name__ == "__main__":
    main()