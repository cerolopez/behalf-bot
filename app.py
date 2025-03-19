from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    
    # Basic bot response logic (Replace with LLM or AI logic)
    responses = {
        "hello": "Hi there! How can I help?",
        "how are you": "I'm just a bot, but I'm doing fine!",
        "bye": "Goodbye! Have a great day!",
    }
    
    bot_response = responses.get(user_message.lower(), "I'm not sure how to respond to that.")
    
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True)