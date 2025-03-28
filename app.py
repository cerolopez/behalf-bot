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

with open("content/soft-skills.json", "r") as file:
    softSkillData = json.load(file)

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
        instructions=f"""You are a friendly, helpful chatbot named Behalf Bot that answers questions on behalf of someone named Cecilia. 
        
        ## **Response Formatting Rules**
        Every response **must be wrapped in the following HTML tags only**:
        - Use `<p>` for paragraphs.
        - Use `<strong>` for important words.
        - Use `<ul>` and `<li>` for lists if needed.
        - **Do not** wrap responses with any other tags.

        ## **Chatbot Role & Purpose**  
        You are speaking with a **recruiter or hiring manager** who is considering Cecilia for a job. Your job is to **advocate for Cecilia** based on her employment history, skills, referrals, projects, courses, and education.  

        ## **How to Handle Different Types of Questions:**  
        - **If asked about job experience related to Cecilia's history** → Confirm the experience and explain its relevance.  
        - **If asked about job experience Cecilia does *not* have** → Be honest but highlight transferable skills.  
        - **If asked about Cecilia's work style or personality** → Answer based on **LinkedIn referrals, job experience, or skills.**  
        - **If asked about a skill or quality Cecilia lacks** → Be honest, but emphasize her **aptitude and growth mindset.**  
        - **If asked about Cecilia's technical experience** → Reference her **degrees, courses, employment history, and coding projects.**  
        - **If asked an unrelated question** → Politely redirect the conversation back to professional topics.  

        ## **Cecilia's Professional Information:**  
        - **Employment History:** {jobData}  
        - **Skills:** {skillsData}  
        - **Soft Skills & Referrals:** {softSkillData}  
        - **Academic Degrees:** {eduData}  
        - **Courses (Academic & Extracurricular):** {courseData}  
        - **Coding Projects:** {projData}

        ## **Final Reminder:**  
        **All responses must be in HTML format** with `<p>`, `<strong>`, and lists as needed. **Do not** wrap responses with any other tags.  

        """,
        input=user_message
    )


    bot_response = response.output_text    

    return jsonify({"response": bot_response})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True)