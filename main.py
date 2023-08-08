from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
import os
import openai

openai.api_key = "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"


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://2021pceaddharamveer012:Veeer426@cluster0.9en5ghq.mongodb.net/Chatgpt"
mongo = PyMongo(app)


@app.route("/")
def home():
    chats = mongo.db.chats.find({})
    myChats = [chat for chat in chats]
    print(chats)
    return render_template("index.html", myChats=myChats)


@app.route("/api", methods=["GET", "POST"])
def qa():
    if request.method == "POST":
        print(request.json)
        question = request.json.get("question")
        chat = mongo.db.chats.find_one({"question": question})
        print(chat)
        if chat:
            data = {"question": question, "answer": f"{chat['answer']}"}
            return jsonify(data)
        else:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=question,
                temperature=1,
                max_tokens=256,
                top_p=1, 
                frequency_penalty=0,
                presence_penalty=0
            )
            print(response)
            data = {"question": question,
                    "answer": response["choices"][0]["text"]}
            mongo.db.chats.insert_one(
                {"question": question, "answer": response["choices"][0]["text"]})
            return jsonify(data)
    data = {"result": "I'm just a computer program, so I don't have feelings, but I'm here and ready to help you with any questions or tasks you have. How can I assist you today?"}
    return jsonify(data)


app.run(debug=True)
