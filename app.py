from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50"
headers = {"Authorization": "Bearer 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"}

def query(image_file):
    # Send the image file directly to the Hugging Face API
    response = requests.post(API_URL, headers=headers, data=image_file)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file is uploaded
        if 'photo' not in request.files:
            return render_template('index.html', result="No file part in the request.")
        
        file = request.files['photo']

        # Check if a file is selected
        if file.filename == '':
            return render_template('index.html', result="No file selected.")
        
        # Read the file in binary mode
        file_data = file.read()

        # Query the Hugging Face API
        output = query(file_data)

        # Handle errors or display results
        if "error" in output:
            return render_template('index.html', result=f"Error: {output['error']}")
        else:
            # Extract the label from the API response
            label = output[0].get('label', 'Unknown')
            return render_template('index.html', result=f"Detected Object: {label}")

    # GET request: Render the upload form
    return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run(debug=True)
