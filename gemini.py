import os
import google.generativeai as genai

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def gemini_generate(prompt):
  try:
    response = model.generate_content(prompt)
    return response.text
  except:
    return None