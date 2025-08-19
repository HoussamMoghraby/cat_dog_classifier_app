from flask import Flask, request, render_template_string
from model import ObjectDetector
import os

app = Flask(__name__)
model = ObjectDetector('yolov8n.pt')

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Object Detection - Cat & Dog Detector</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px 0;
        }
        .container {
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 800px;
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
        <h2>Object Detection - Cat & Dog Detector</h2>
        <form method="post" enctype="multipart/form-data">
            <div class="upload-area">
                <div class="upload-icon">📁</div>
                <p class="upload-label">Drag and drop an image or click to browse</p>
                <input type="file" name="file" class="file-input" accept="image/*">
            </div>
            <button type="submit" class="btn-upload">Detect Objects</button>
        </form>
        {% if result_image %}
        <div class="prediction">
            <h3>{{ detection_result }}</h3>
            <div class="result-image" style="margin-top: 15px;">
                <img src="data:image/jpeg;base64,{{ result_image }}" style="max-width:100%; border-radius:5px;">
            </div>
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
    result_image = None
    detection_result = None
    
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filepath = os.path.join('input.jpg')
            file.save(filepath)
            
            # Use YOLOv8 for object detection
            result_image, detection_result, _ = model.detect(filepath)
            
    return render_template_string(HTML, result_image=result_image, detection_result=detection_result)

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=6000, debug=False)