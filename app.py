from flask import Flask, request, render_template
import doctr
from PIL import Image
import io
from pdf2image import convert_from_bytes

app = Flask(__name__)

def perform_ocr_on_image(image):
    model = doctr.models.predictor('crnn_vgg16_bn', pretrained=True)
    result = model([image])
    return result[0]['value']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'

        if file:
            extracted_text = ''
            if file.filename.endswith('.pdf'):
                # Convert PDF to images
                images = convert_from_bytes(file.read())
                for image in images:
                    extracted_text += perform_ocr_on_image(image) + '\n'
            else:
                # Handle other image types
                image = Image.open(io.BytesIO(file.read()))
                extracted_text = perform_ocr_on_image(image)

            return f'Text extracted: {extracted_text}'
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=False)
