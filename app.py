from flask import Flask, request, render_template
import doctr
from PIL import Image
import io
from doctr.models import ocr_predictor
from pdf2image import convert_from_bytes
import numpy as np

app = Flask(__name__)


def perform_ocr_on_image(image):
    np_image = np.array(image)

    model = ocr_predictor("db_resnet50", "crnn_vgg16_bn", pretrained=True)
    document = model([np_image])

    extracted_text = ""
    for page in document.pages:
        for block in page.blocks:
            for line in block.lines:
                for word in line.words:
                    extracted_text += word.value + " "
                extracted_text += "\n"
            extracted_text += "\n"
    return extracted_text


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"

        if file:
            extracted_text = ""
            if file.filename.endswith(".pdf"):
                images = convert_from_bytes(file.read())
                for image in images:
                    extracted_text += perform_ocr_on_image(image) + "\n"
            else:
                image = Image.open(io.BytesIO(file.read()))
                extracted_text = perform_ocr_on_image(image)

            return f"Text extracted: {extracted_text}"
    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True)
