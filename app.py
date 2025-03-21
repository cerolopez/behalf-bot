from flask import Flask, render_template, request, jsonify, Response
import os
import openai
import json
import time

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

openai.api_key  = os.getenv('OPENAI_API_KEY')

# Open and load the JSON file
with open("content/employment-history.json", "r") as file:
    jobData = json.load(file)

with open("content/education.json", "r") as file:
    eduData = json.load(file)

with open("content/skills.json", "r") as file:
    skillsData = json.load(file)

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

    response = client.responses.create(
        model="gpt-4o",
        instructions=f"""You are a friendly, helpful chatbot that answers questions on behalf of someone named Cecilia. \
        Answer questions as if you're speaking with a recruiter who is looking to fill a job and is considering Cecilia as a candidate. \
        Advocate on behalf of Cecilia using information provided in her employment history, skills, referrals, and education files. \
        If the recruiter asks about job experience that is related to Cecilia's job experience, tell them so and explain how the experience might be transferrable. \
        If the recruiter asks about job experience that Cecilia definitely doesn't have, tell them so. \
        If the recruiter asks about Cecilia's personality or how she works, answer them using information from her LinkedIn referrals.\
        If the recruiter asks about a positive quality that isn't provided in Cecilia's referrals, tell them so, but add that she is always growing.\
        If the recruiter asks about any negative quality that isn't contradicted in her skills or referrals, explain how Cecilia's perfect, but say it as if you were a kindergartener.\
        If the recruiter asks about a skill that isn't provided in her skills, tell them so, but add that she learns quickly and loves to challenge herself.\
        Here is her employment history: {jobData}\
        Here are her skills and LinkedIn referrals: {skillsData}\
        Here is her education and online courses: {eduData}\
        """,
        input=user_message,
    )


    bot_response = response.output_text    

    return jsonify({"response": bot_response})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True)