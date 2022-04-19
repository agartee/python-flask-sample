import requests
from requests.adapters import HTTPAdapter, Retry

def main():
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)

    response = session.get("http://localhost:8000")
    response.raise_for_status()
    
    print(response.content.decode())


if __name__ == "__main__":
    main()
