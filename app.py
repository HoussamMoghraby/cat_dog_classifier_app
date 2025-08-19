from flask import Flask, request, render_template_string
from model import CatDogClassifier
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import os

app = Flask(__name__)
model = CatDogClassifier('model.h5')

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cat or Dog Classifier</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 500px;
            width: 90%;
        }
        h2 {
            color: #3a3a3a;
            margin-bottom: 2rem;
        }
        .upload-area {
            border: 2px dashed #c3cfe2;
            border-radius: 8px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            position: relative;
        }
        .file-input {
            opacity: 0;
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            cursor: pointer;
        }
        .upload-label {
            font-size: 1rem;
            color: #666;
        }
        .upload-icon {
            font-size: 3rem;
            color: #c3cfe2;
            margin-bottom: 1rem;
        }
        .btn-upload {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0.8rem 2rem;
            border-radius: 50px;
            font-size: 1rem;
            cursor: pointer;
            transition: transform 0.3s ease;
        }
        .btn-upload:hover {
            transform: translateY(-2px);
        }
        .prediction {
            margin-top: 1.5rem;
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 8px;
        }
        .prediction h3 {
            margin: 0;
            color: #4a4a4a;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Cat or Dog Classifier</h2>
        <form method="post" enctype="multipart/form-data">
            <div class="upload-area">
                <div class="upload-icon">📁</div>
                <p class="upload-label">Drag and drop an image or click to browse</p>
                <input type="file" name="file" class="file-input" accept="image/*">
            </div>
            <button type="submit" class="btn-upload">Classify Image</button>
        </form>
        {% if prediction %}
        <div class="prediction">
            <h3>Prediction: {{ prediction }}</h3>
        </div>
        {% endif %}
    </div>

    <script>
        // Display selected file name
        document.querySelector('.file-input').addEventListener('change', function(e) {
            if(e.target.files.length > 0) {
                document.querySelector('.upload-label').textContent = e.target.files[0].name;
            }
        });
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    prediction = None
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filepath = os.path.join('input.jpg')
            file.save(filepath)
            # Use the model to predict
            img = load_img(filepath, target_size=(224, 224))
            img = img_to_array(img)
            img = img.reshape(1, 224, 224, 3)
            result = model.model.predict(img)
            prediction = "Cat" if result[0] == 0 else "Dog"
    return render_template_string(HTML, prediction=prediction)

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=False)