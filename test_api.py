import requests

data = {
    "message": "I am really happy",
}

while True:
    url = "http://localhost/accuracy"

    response = requests.post(url=url, json=data)
