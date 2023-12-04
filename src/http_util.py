import requests


class HttpUtils:

    def __init__(self,url: str):
        self.url = url;
    
    def get_json_from_endpoint(self,endpoint:str):

        url = self.url + "/" + endpoint
        try:
            response = requests.get(url)
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse JSON data
                json_data = response.json()
                return json_data
            else:
                print(f"Failed to retrieve data. Status code: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return None
