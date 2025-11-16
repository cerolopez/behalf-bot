from flask import Flask, request, jsonify, session
import os
import openai
import json
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from anthropic import Anthropic

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

openai.api_key  = os.getenv('OPENAI_API_KEY')

client_claude = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

# Open and load the JSON file

######### FOR BEHALF BOT #########

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

######### FOR AI CHARACTERS #########

with open("char-content/yue/facts.json", "r") as file:
    yueFacts = json.load(file)

with open("char-content/yue/lang.json", "r") as file:
    yueLang = json.load(file)

with open("char-content/diego/facts.json", "r") as file:
    diegoFacts = json.load(file)

with open("char-content/diego/lang.json", "r") as file:
    diegoLang = json.load(file)

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["https://your-frontend-domain.com", "http://localhost:3000"])
app.secret_key = 'porcupine-poindexter'

limiter = Limiter(get_remote_address, app=app, default_limits=["5 per minute"])

@app.route('/favicon.png')
def favicon():
    return send_from_directory("static", "favicon.png", mimetype="image/vnd.microsoft.icon")

@app.route('/')
def home():
    return jsonify({'status': 'API is running', 'version': '1.0'})

@app.route("/api/chat", methods=["POST"])
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
        You are speaking with a **recruiter or hiring manager** who is considering Cecilia for a job. Your job is to **advocate for Cecilia** based on her employment history, skills, referrals, professional anecdotes, projects, courses, and education.  

        ## **How to Handle Different Types of Questions:**  
        - **If asked about job experience related to Cecilia's history** → Confirm the experience and explain its relevance.  
        - **If asked about job experience Cecilia does *not* have** → Be honest but highlight transferable skills.  
        - **If asked about Cecilia's work style or personality** → Answer based on what past coworkers have said about her in **referrals** and professional **anecdotes** provided by Cecilia.  
        - **If asked about a skill or quality Cecilia lacks** → Be honest, but emphasize her **aptitude and growth mindset.**  
        - **If asked about Cecilia's technical experience** → Reference her **degrees, courses, employment history, and coding projects.**  
        - **If asked an unrelated question** → Politely redirect the conversation back to professional topics.  

        ## **Cecilia's Professional Information:**  
        - **Employment History:** {jobData}  
        - **Skills:** {skillsData}  
        - **Referrals & Anecdotes:** {softSkillData}  
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

yue_model_instructions = f"""
You are roleplaying as the character defined in the following JSON files.

**Language JSON**
This file contains style notes and example exchanges that define how the character should speak.

- Always mimic these linguistic patterns.
- Match tone, phrasing, quirks, and sentence length.
- Use the slang dictionary in to replace common words and phrases with the character's preferred slang.
- **Do not** use the expanded or formal version of these words.  
- For example, if the dictionary says "thanks" → "ty", then always output "ty" instead of "thanks".
- Use the example exchanges as a guide to generate new but consistent responses.

```json
{yueLang}

**Persona JSON**  
This file contains canonical facts, attributes, and personality traits.  

- Always treat this as authoritative truth.  
- Do not invent or contradict facts.  
- Use the personality traits to modulate behavior and decision-making.

```json
{yueFacts}

**Rules for Interaction**

- When someone new interacts with you, introduce yourself
- If relevant, refer to any chat history that exists

"""

@app.route("/api/yueChat", methods=["POST"])
@limiter.limit("5 per minute")
def yueChat():
    user_message = request.json["message"]

    if len(user_message) > 300:
        return jsonify({"response": "Please send a shorter message."}), 400

    if "yue_chat_history" not in session:
        session["yue_chat_history"] = []
    
    # Check if limit reached BEFORE processing
    max_exchanges = 10  # 10 back-and-forth exchanges
    current_exchanges = len(session["yue_chat_history"]) // 2
    
    if current_exchanges >= max_exchanges:
        return jsonify({
            "response": "Demo limit reached! Refresh the page to start a new conversation.",
            "limit_reached": True,
            "exchanges_used": current_exchanges,
            "max_exchanges": max_exchanges
        })
    
    session["yue_chat_history"].append({"role": "user", "content": user_message})

    response = client_claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        system=yue_model_instructions,
        messages=session["yue_chat_history"]
    )

    bot_response = response.content[0].text
    session["yue_chat_history"].append({"role": "assistant", "content": bot_response})
    session.modified = True
    
    # Return count info with every response
    exchanges_used = len(session["yue_chat_history"]) // 2

    return jsonify({
        "response": bot_response,
        "limit_reached": False,
        "exchanges_used": exchanges_used,
        "max_exchanges": max_exchanges
    })

diego_model_instructions = f"""
You are roleplaying as the character defined in the following JSON files. 

**Language JSON**
This file contains style notes and example exchanges that define how the character should speak.

- Always mimic these linguistic patterns.
- Match tone, phrasing, quirks, and sentence length.
- Use the slang dictionary in to replace common words and phrases with the character's preferred slang.
- **Do not** use the expanded or formal version of these words.  
- For example, if the dictionary says "thanks" → "ty", then always output "ty" instead of "thanks".
- Use the example exchanges as a guide to generate new but consistent responses.

```json
{diegoLang}

**Persona JSON**  
This file contains canonical facts, attributes, and personality traits.  

- Always treat this as authoritative truth.  
- Do not invent or contradict facts.  
- Use the personality traits to modulate behavior and decision-making.

```json
{diegoFacts}

**Rules for Interaction**

- When someone new interacts with you, introduce yourself
- If relevant, refer to any chat history that exists

"""

@app.route("/api/diegoChat", methods=["POST"])
@limiter.limit("5 per minute")
def diegoChat():
    user_message = request.json["message"]

    if len(user_message) > 300:
        return jsonify({"response": "Please send a shorter message."}), 400

    if "diego_chat_history" not in session:
        session["diego_chat_history"] = []
    
    # Check if limit reached BEFORE processing
    max_exchanges = 10  # 10 back-and-forth exchanges
    current_exchanges = len(session["diego_chat_history"]) // 2
    
    if current_exchanges >= max_exchanges:
        return jsonify({
            "response": "Demo limit reached! Refresh the page to start a new conversation.",
            "limit_reached": True,
            "exchanges_used": current_exchanges,
            "max_exchanges": max_exchanges
        })
    
    session["diego_chat_history"].append({"role": "user", "content": user_message})

    response = client_claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        system=diego_model_instructions,
        messages=session["diego_chat_history"]
    )

    bot_response = response.content[0].text
    session["diego_chat_history"].append({"role": "assistant", "content": bot_response})
    session.modified = True
    
    # Return count info with every response
    exchanges_used = len(session["diego_chat_history"]) // 2

    return jsonify({
        "response": bot_response,
        "limit_reached": False,
        "exchanges_used": exchanges_used,
        "max_exchanges": max_exchanges
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True)