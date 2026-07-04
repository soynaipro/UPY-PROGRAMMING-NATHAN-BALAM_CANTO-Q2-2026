from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

class EduAgent:
    def __init__(self):
        # La nueva forma de conectarse a la API de Gemini
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def chunk_text(self, text, size=2000):
        """Divide el texto en fragmentos para evitar límites de tokens."""
        return [text[i:i+size] for i in range(0, len(text), size)]

    def generate_quiz(self, study_material, difficulty="Medium"):
        """El Agente percibe el texto y actúa generando un quiz estructurado."""
        chunks = self.chunk_text(study_material)
        prompt = f"""
        Acting as an Educational Agent, analyze this text and create 3 multiple-choice questions.
        Difficulty: {difficulty}
        Text: {chunks[0]}
        
        Format your response strictly as:
        Q: [Question]
        A) [Option]
        B) [Option]
        C) [Option]
        Correct: [Letter]
        Rationale: [Explanation]
        """
        
        # Usamos el modelo más nuevo y rápido de texto
        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text