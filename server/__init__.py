
import os
import os.path as osp
from flask import Flask
from flask import request
from PyPDF2 import PdfReader
from transformers import AutoModelForQuestionAnswering
from transformers import AutoTokenizer
from transformers import pipeline
from werkzeug.utils import secure_filename

# Import model
model_name = "deepset/roberta-base-squad2"
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

# Create GUI
def create_app():
    app = Flask(__name__)

    _base = osp.abspath(osp.dirname(__file__))
    app.config["UPLOAD_FOLDER"] = osp.join(_base, "upload")

    # Setup folders
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Upload files
    @app.route("/upload", methods=["POST"])
    def upload():
        f = request.files["file"]
        filename = secure_filename(f.filename)

        f.save(osp.join(app.config['UPLOAD_FOLDER'], filename))
        return { "message": "Upload Success" }, 201

    # Get questions
    @app.route("/ask", methods=["POST"])
    def answer():

        # Get filename and question
        data = request.get_json()
        filename = osp.join(app.config['UPLOAD_FOLDER'], data["filename"])
        question = data["question"]

        # Extract text from PDF file
        reader = PdfReader(filename)
        context = ""
        for page in reader.pages:
            text = page.extract_text()
            context = context + text + " "

        # Feed question and context into a input of which the model can eat
        QA_input = { 'question': question, 'context': context}

        # Get prediction and its confidence score from the model
        res = nlp(QA_input)
        answer = res["answer"]

        return { "answer": answer }

    return app
