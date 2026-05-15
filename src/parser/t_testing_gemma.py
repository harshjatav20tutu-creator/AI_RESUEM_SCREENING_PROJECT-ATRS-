import requests
import json

# Define the local address of your Ollama server
def testing(url):
    prompt_text = "Extract the name from this text: 'Contact: Rajesh Kumar, Software Engineer'. Return a python dictionary which contain key = 'candiate_name' and value = 'extracted_name' make sure don not say somethin just return a dictionary."
    payload = {
        "model": "gemma2:2b",
        "prompt": prompt_text,
        "stream": False
    }

    # Sending the request to the server
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        # Convert the raw response into a Python dictionary
        data = response.json()
        
        # The actual answer from Gemma is stored in the 'response' key
        answer = data.get("response")
        return answer
    else:
        print(f"Error: {response.status_code}")

OLLAMA_URL = "http://localhost:11434/api/generate"
print(testing(OLLAMA_URL))