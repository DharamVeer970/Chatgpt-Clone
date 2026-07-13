from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

OPENAI_MODEL = os.environ.get("OPENAI_MODEL")
client = OpenAI() if os.environ.get("OPENAI_API_KEY") else None


app = Flask(__name__)
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
# No MONGO_URI -> run without persistence so the UI still boots.
mongo = PyMongo(app) if app.config["MONGO_URI"] else None


@app.route("/")
def home():
    myChats = list(mongo.db.chats.find({})) if mongo else []
    return render_template("index.html", myChats=myChats)


@app.route("/api", methods=["POST"])
def qa():
    question = request.json.get("question")

    chat = mongo.db.chats.find_one({"question": question}) if mongo else None
    if chat:
        return jsonify({"question": question, "answer": chat["answer"]})

    if not client:
        return jsonify({
            "question": question,
            "answer": "No OPENAI_API_KEY set - running in UI-only mode.",
        })
    if not OPENAI_MODEL:
        return jsonify({
            "question": question,
            "answer": "No OPENAI_MODEL set - add one to your .env.",
        })

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": question}],
        temperature=1,
        max_tokens=256,
    )
    answer = response.choices[0].message.content
    if mongo:
        mongo.db.chats.insert_one({"question": question, "answer": answer})
    return jsonify({"question": question, "answer": answer})


if __name__ == "__main__":
    app.run(debug=True)
