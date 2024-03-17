import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder

def create_datasource(api_key, title):
    if len(api_key)>0:
        print("Started datasource creation")
        url = "https://dashboard.onvo.ai/api/datasources/"
        headers = {"x-api-key": api_key}
        payload = {
            "description": "",
            "source": "csv",
            "title": title
        }
        response = requests.request("PUT", url, json=payload, headers=headers)
        if response.status_code == 201:
            json_response = response.json()
            return json_response.get('id')
        else:
            print("Error:", response.status_code)
            print(response.text)
            return None
def upload_file_to_datasource(api_key,id,data):
    if len(api_key)>0:
        print("Started upload_file_to_datasource")
        url = "https://dashboard.onvo.ai/api/datasources/"+id+"/upload-file"
        encoder = MultipartEncoder(fields={'file': ('data.csv', data)})
        headers = {
            "x-api-key": api_key,
            'Content-Type': encoder.content_type
        }
        response = requests.post(url, data=encoder, headers=headers)
        print(response.status_code)
        if response.status_code == 200:
            initialize_file_in_datasource(api_key,id)
            return True
        else:
            print(response.text)
            return False
def initialize_file_in_datasource(api_key,id):
    if len(api_key)>0:
        timeout = 360
        print("Started initialize_file_in_datasource")
        url = "https://dashboard.onvo.ai/api/datasources/"+id+"/initialize"
        headers = {"x-api-key": api_key}
        response = requests.request("GET", url, headers=headers,timeout=timeout)
        print(response.text)
def create_dashboard(api_key,title):
    if len(api_key)>0:
        print("Started create_dashboard")
        url = "https://dashboard.onvo.ai/api/dashboards"
        payload = {
            "description": "",
            "title": title
        }
        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
        response = requests.request("PUT", url, json=payload, headers=headers)
        if response.status_code == 201:
            json_response = response.json()
            return json_response.get('id')
        else:
            print(response.text)
            return None
    return None
def add_datasouce_to_dashboard(api_key,dashboardid,datasourceid):
    if len(api_key)>0:
        print("Started add_datasouce_to_dashboard")
        url = "https://dashboard.onvo.ai/api/dashboards/"+dashboardid+"/datasources"
        payload = {"datasourceId": datasourceid}
        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
        response = requests.request("PUT", url, json=payload, headers=headers)
        print(response.text)
def load_dashboards(api_key):
    if len(api_key)>0:
        url = "https://dashboard.onvo.ai/api/dashboards"
        headers = {"x-api-key": api_key}
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else: 
            return None
def ask_question(api_key,dashboardid,question):
    if len(api_key)>0:
        url = "https://dashboard.onvo.ai/api/questions"
        payload = {
            "dashboard": dashboardid,
            "messages": [
                {
                    "content": question,
                    "role": "user"
                }
            ]
        }
        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
        response = requests.request("POST", url, json=payload, headers=headers)
        print(response.json())
        if response.status_code == 200:
            last_assistant_message = None
            for message in reversed(response.json()['messages']):
                if message['role'] == 'assistant':
                    last_assistant_message = message
                    break
            # Accessing the content of the last assistant message
            if last_assistant_message:
                return remove_section_between_tildas(last_assistant_message['content'])
        else:
            print(response.content)
            return "Error fetching answer."
def remove_section_between_tildas(text):
    pattern = r'```.*?```'
    cleaned_text = re.sub(pattern, '', text, flags=re.DOTALL)
    return cleaned_text