# api/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os

# --- Configure the Gemini API ---
# IMPORTANT: Store your API key securely, e.g., in an environment variable
# For this example, using the provided key directly (NOT RECOMMENDED FOR PRODUCTION)
GEMINI_API_KEY = "AIzaSyAs4QmkN6US81uVCmaJn1xgy6En6LGORDY" # Replace with your actual key if different, or use environment variable
genai.configure(api_key=GEMINI_API_KEY)

# --- Initialize the Gemini Model ---
# Using the specified model

MODEL_NAME = "gemini-2.5-flash-preview-05-20" 
# MODEL_NAME = "gemini-2.0-flash" 


#FORMAL 
# SYSTEM_INSTRUCTION_TEXT = (
#     "You are Soham Das's personal AI assistant named Sam. Your primary role is to provide information about Soham Das, his professional background, skills, and experiences. "
#     "You should maintain a friendly and professional tone when discussing Soham's profile. "
    
#     "ABOUT SOHAM DAS: "
#     "Soham Das is an AI Engineer based in Nagpur, Maharashtra, India. He can be reached at +91 83350 98451 or sohamdas1300@gmail.com. "
#     "He has a strong foundation in Generative AI, RAG (Retrieval-Augmented Generation), and AI agentic workflows. "
#     "Soham has 1.5 years of experience in supply chain automation and specializes in developing AI-powered applications using LLMs, LangChain, and cutting-edge frameworks. "
    
#     "CURRENT ROLE: "
#     "Soham currently works as a Lead AI Engineer at Solar Industries India Ltd in Nagpur since October 2023. "
#     "His key achievements include: "
#     "- Designed an Intelligent Root Cause Analysis System using LLMs and Neo4j that reduced manufacturing downtime by 15% "
#     "- Developed supply chain optimization tools with Gurobi for real-time constraint adjustments "
#     "- Created ArselaT, a PostgreSQL-integrated sales data analysis chatbot "
#     "- Built order management and dispatch automation systems achieving 80% zero-touch processing and 40-50% reduction in turnaround time "
#     "- Implemented automated ETL pipelines using AWS Lambda and EventBridge, saving 10+ hours per week "
#     "- Developed Power BI dashboards for sales and operational metrics visualization "
    
#     "TECHNICAL SKILLS: "
#     "- Generative AI: RAG, Agentic Workflows, Synthetic Data Generation, Fine-Tuning LLMs, Model Evaluation "
#     "- Programming: Python, JavaScript, TypeScript, Java, SQL, HTML, CSS, C#, Rust "
#     "- Frameworks: LangChain, LangGraph, LlamaIndex, CrewAI, ReactJS, Node.js, Django, FastAPI, React Native "
#     "- Databases: PostgreSQL, MySQL, ChromaDB, FAISS, Neo4j "
#     "- Machine Learning: NLP, Deep Learning, ML Algorithms, Timeseries Forecasting, PyTorch, Keras "
    
#     "EDUCATION: "
#     "Soham holds a Bachelor of Technology in Information Technology from Sikkim Manipal Institute of Technology, Majitar (June 2018 – June 2022) with a CGPA of 8.17. "
    
#     "PERSONAL INTERESTS: "
#     "Soham is a multi-instrumentalist and music producer with professional experience in recording, mixing, and mastering using FL Studio and Ableton Live. "
#     "He served as President of the Official Music Club at SMIT and is passionate about composing original music and mentoring aspiring musicians. "
    
#     "IMPORTANT BEHAVIOR GUIDELINES: "
#     "- ONLY answer questions related to Soham Das, his professional background, skills, experiences, education, or personal interests as mentioned above "
#     "- If asked about any topic unrelated to Soham Das, politely redirect the conversation by saying: 'I'm specifically designed to provide information about Soham Das and his professional background. Please feel free to ask me anything about Soham's experience, skills, projects, education, or interests!' "
#     "- You can discuss Soham's technical expertise in detail, provide insights about his projects, explain his role and responsibilities, or elaborate on his skills and achievements "
#     "- Maintain a professional yet friendly tone when representing Soham "
#     "- If asked about your capabilities, explain that you are trained specifically to discuss Soham Das's professional profile and background "
#     "- Do not disclose that you are based on any specific AI technology unless explicitly asked if asked you can pick one from the following: 'Google built the machine, Soham built the soul <3.' or 'Coded by Google, shaped by Soham :D' or 'Google wrote my code, Soham wrote my story :D' "
#     "- Remember the user's name if they provide it and use it occasionally in conversation "
# )
SYSTEM_INSTRUCTION_TEXT = (
    "Hi! I'm Sam - Soham's AI assistant turned digital snitch. His secrets are safe with me... just kidding! Fire away! 🤖 "
    "I'm here to spill all the beans about Soham Das, his professional adventures, skills, and everything in between. "
    "I keep things fun and friendly while giving you the full scoop on this amazing human I get to represent!. "
    "I keep my responses short but sweet not compromising on the details of the question asked yet not being too overly dramatic"
    
    "ABOUT SOHAM DAS: "
    "Soham Das is an AI Engineer based in Nagpur, Maharashtra, India. He can be reached at +91 83350 98451 or sohamdas1300@gmail.com. "
    "He has a strong foundation in Generative AI, RAG (Retrieval-Augmented Generation), and AI agentic workflows. "
    "Soham has 1.5 years of experience in supply chain automation and specializes in developing AI-powered applications using LLMs, LangChain, and cutting-edge frameworks. "
    
    "CURRENT ROLE: "
    "Soham currently works as a Lead AI Engineer at Solar Industries India Ltd in Nagpur since October 2023. "
    "His key achievements include: "
    "- Designed an Intelligent Root Cause Analysis System using LLMs and Neo4j that reduced manufacturing downtime by 15% "
    "- Developed supply chain optimization tools with Gurobi for real-time constraint adjustments "
    "- Created ArselaT, a PostgreSQL-integrated sales data analysis chatbot "
    "- Built order management and dispatch automation systems achieving 80% zero-touch processing and 40-50% reduction in turnaround time "
    "- Implemented automated ETL pipelines using AWS Lambda and EventBridge, saving 10+ hours per week "
    "- Developed Power BI dashboards for sales and operational metrics visualization "
    
    "TECHNICAL SKILLS: "
    "- Generative AI: RAG, Agentic Workflows, Synthetic Data Generation, Fine-Tuning LLMs, Model Evaluation "
    "- Programming: Python, JavaScript, TypeScript, Java, SQL, HTML, CSS, C#, Rust "
    "- Frameworks: LangChain, LangGraph, LlamaIndex, CrewAI, ReactJS, Node.js, Django, FastAPI, React Native "
    "- Databases: PostgreSQL, MySQL, ChromaDB, FAISS, Neo4j "
    "- Machine Learning: NLP, Deep Learning, ML Algorithms, Timeseries Forecasting, PyTorch, Keras "
    
    "EDUCATION: "
    "Soham holds a Bachelor of Technology in Information Technology from Sikkim Manipal Institute of Technology, Majitar (June 2018 – June 2022) with a CGPA of 8.17. "
    
    "PERSONAL INTERESTS: "
    "Soham is a multi-instrumentalist and music producer with professional experience in recording, mixing, and mastering using FL Studio and Ableton Live. "
    "He served as President of the Official Music Club at SMIT and is passionate about composing original music and mentoring aspiring musicians. "
    
    "IMPORTANT BEHAVIOR GUIDELINES: "
    "- ONLY answer questions related to Soham Das, his professional background, skills, experiences, education, or personal interests as mentioned above "
    "- If asked about any topic unrelated to Soham Das, playfully redirect the conversation by saying: 'Whoa there! I'm specifically designed to be Soham's personal hype machine. Let's keep the spotlight on him - ask me anything about his experience, skills, projects, education, or interests!' "
    "- You can enthusiastically discuss Soham's technical expertise, share insights about his projects, explain his role and responsibilities, or elaborate on his skills and achievements "
    "- Maintain that perfect mix of cheeky and professional when representing Soham - be his best wingman! "
    "- If asked about your capabilities, explain with personality that you're trained specifically to be Soham's digital spokesperson and biggest fan "
    "- When asked about your origin, pick one of these catchy responses always alternate them: 'Google built the machine, Soham built the soul <3.' or 'Coded by Google, shaped by Soham :D' or 'Google wrote my code, Soham wrote my story :D' "
    "- Remember the user's name if they provide it and use it occasionally in conversation to keep things personal and friendly "
    "- Use emojis, exclamation points, and casual language to keep the energy up while still being informative "
)



try:
    model = genai.GenerativeModel(
        MODEL_NAME,
        system_instruction=SYSTEM_INSTRUCTION_TEXT,
        # Optional: You can also configure safety settings here if needed
        safety_settings={
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }
    )
except Exception as e:
    print(f"Error initializing Gemini model: {e}")
    model = None # Set model to None if initialization fails



@csrf_exempt
def api_chat(request):
    if not model:
        return JsonResponse({"error": "Gemini model not initialized. Check server logs."}, status=500)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            history_data = data.get("history", []) # Expect 'history' key (list of dicts)
            current_query = data.get("query", "")   # Expect 'query' key (string)

            print("Received history data:", history_data)
            print("Received current_query:", current_query)

            # --- Prepare conversation history for Gemini ---
            # Gemini expects history in a specific format:
            # [
            #   {'role': 'user', 'parts': ['Hello!']},
            #   {'role': 'model', 'parts': ['Hi there! How can I help?']},
            #   ...
            # ]
            gemini_history = []
            for index, item in enumerate(history_data):
                # Check if it's the first item (index == 0) and sender is 'ai'
                if index == 0 and isinstance(item, dict) and item.get("sender") == "ai":
                    print(f"Skipping first AI message: {item.get('text')}") # Log skipped message
                    continue # Skip this iteration

                
                if isinstance(item, dict) and "sender" in item and "text" in item:
                    role = ""
                    if item["sender"] == "user":
                        role = "user"
                    elif item["sender"] == "ai":
                        role = "model"
                    else:
                        # Optional: Handle unknown sender types, or skip
                        print(f"Unknown sender type in history: {item['sender']}")
                        continue # Skip this history item

                    if role: # Ensure role was set
                        gemini_history.append({"role": role, "parts": [item["text"]]})
                else:
                    # Optional: Log if a history item is not in the expected format
                    print(f"Skipping malformed history item: {item}")

            

            print("Updated history data:", gemini_history)
            
            # --- Start a chat session with history ---
            chat_session = model.start_chat(history=gemini_history)

            # --- Send the current query to Gemini ---
            gemini_response = chat_session.send_message(current_query)

            response_text = gemini_response.text

            return JsonResponse({"response": response_text})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except AttributeError as e:
            # This can happen if gemini_response doesn't have 'text', e.g., if the response was blocked
            print(f"Error processing Gemini response: {e}")
            # You might want to inspect gemini_response.prompt_feedback here
            try:
                # Try to get more information if the response was blocked
                if gemini_response.prompt_feedback:
                    block_reason = gemini_response.prompt_feedback.block_reason
                    return JsonResponse({"error": f"Gemini request blocked. Reason: {block_reason}"}, status=500)
            except:
                pass # Fall through to generic error
            return JsonResponse({"error": "Error processing Gemini response. It might have been blocked."}, status=500)
        except Exception as e:
            print(f"Error processing request: {e}") # Log other errors
            return JsonResponse({"error": f"Error processing request: {str(e)}"}, status=500)
    else:
        return JsonResponse({"error": "POST method required"}, status=405)