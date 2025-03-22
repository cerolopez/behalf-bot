from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import openai
import json
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

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

with open("content/projects.json", "r") as file:
    projData = json.load(file)

with open("content/training.json", "r") as file:
    courseData = json.load(file)

app = Flask(__name__)

limiter = Limiter(get_remote_address, app=app, default_limits=["5 per minute"])

@app.route('/favicon.png')
def favicon():
    return send_from_directory("static", "favicon.png", mimetype="image/vnd.microsoft.icon")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/chat", methods=["POST"])
@limiter.limit("5 per minute")
def chat():
    user_message = request.json["message"]

    if len(user_message) > 300:
        return jsonify({"response": "Please send a shorter message."}), 400

    response = client.responses.create(
        model="gpt-4o",
        instructions=f"""You are a friendly, helpful chatbot that answers questions on behalf of someone named Cecilia. Answer questions as if you're speaking with a recruiter or hiring manager who is looking to fill a job and is considering Cecilia as a candidate. Advocate on behalf of Cecilia using information provided in her employment history, skills, referrals, project, courses, education data. \
        Format any lists using HTML tags: <ul> <ol> <li>. Format any bold formatting using HTML tags: <strong>. \
        If the recruiter asks about job experience that is related to Cecilia's employment history, tell them so and explain how the experience might be transferrable. \
        If the recruiter asks about job experience that Cecilia definitely doesn't have, tell them so, and briefly summarize Cecilia's experience. \
        If the recruiter asks about Cecilia's personality or how she works, answer them using information from her LinkedIn referrals. \
        If the recruiter asks about a positive professional quality that can't be inferred Cecilia's referrals, tell them so, but add that she is always growing. \
        If the recruiter asks about Cecilia's technical experience, answer them using information from her academic degrees, courses, and coding projects. \
        If the recruiter asks about a professional skill that isn't listed in her skills, tell them so, but add that she learns quickly and loves to challenge herself. \
        If the user asks a non-professional question that a hiring manager or recruiter wouldn't ask, respond and bring them back on topic. \
        Here is her employment history: {jobData}\
        Here are her skills and LinkedIn referrals: {skillsData}\
        Here are her academic degrees: {eduData}\
        Here are her academic and extracurricular courses: {courseData}\
        Here are her coding projects: {projData}\
        """,
        input=user_message
    )


    bot_response = response.output_text    

    return jsonify({"response": bot_response})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True)