import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50"
headers = {"Authorization": r"Bearer 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"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

output = query("cats.jpg")

print(output[0]['label'])
