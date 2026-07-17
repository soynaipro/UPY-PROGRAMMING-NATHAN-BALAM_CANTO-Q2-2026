from google import genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

class EduAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def generate_quiz(self, study_material, difficulty="Easy", num_questions=10, language="Spanish"):
        prompt = f"""
        Act as an Educational Agent. Analyze this text and create {num_questions} multiple-choice questions.
        Difficulty: {difficulty}
        Language: {language}
        Text: "{study_material[:3500]}"

        STRICT RULE: Your response MUST be ONLY a valid JSON array, with no extra text before or after. Do not include markdown code block tags if possible. Exact format for each object:
        [
          {{
            "q": "Question text in {language}",
            "options": ["Option A", "Option B", "Option C"],
            "correct": "Exact text of the correct option",
            "rationale": "Brief explanation in {language}",
            "reference": "Short exact quote from text that proves the answer"
          }}
        ]
        """
        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        # Limpieza de seguridad por si la IA agrega etiquetas de código markdown
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        try:
            return json.loads(clean_text)
        except Exception as e:
            print(f"Error parseando JSON: {e}")
            return []