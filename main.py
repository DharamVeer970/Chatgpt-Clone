from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

# `or` not a get() default: a blank var in .env is "" and must still fall back.
OPENAI_MODEL = os.environ.get("OPENAI_MODEL") or "gpt-4o-mini"
client = OpenAI() if os.environ.get("OPENAI_API_KEY") else None


app = Flask(__name__)
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
# No MONGO_URI -> run without persistence so the UI still boots.
mongo = PyMongo(app) if app.config["MONGO_URI"] else None


@app.route("/")
def home():
    myChats = list(mongo.db.chats.find({})) if mongo else []
    return render_template("index.html", myChats=myChats)


@app.route("/api", methods=["GET", "POST"])
def qa():
    if request.method == "POST":
        question = request.json.get("question")

        chat = mongo.db.chats.find_one({"question": question}) if mongo else None
        if chat:
            return jsonify({"question": question, "answer": chat["answer"]})

        if not client:
            return jsonify({
                "question": question,
                "answer": "No OPENAI_API_KEY set - running in UI-only mode.",
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
    data = {"result": "I'm just a computer program, so I don't have feelings, but I'm here and ready to help you with any questions or tasks you have. How can I assist you today?"}
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
