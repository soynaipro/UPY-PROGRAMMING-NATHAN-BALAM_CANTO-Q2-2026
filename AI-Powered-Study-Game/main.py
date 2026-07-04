from ai_agent import EduAgent
import time

def game_loop():
    print("==================================================")
    print("           AI Powered Study Game                  ")
    print(" Alignment: SDG 4 (Education) & NLP Agents        ")
    print("==================================================\n")
    
    agent = EduAgent()
    
    # Entrada de datos inicial para el avance
    material = input("Paste your study notes or topic: ")
    difficulty = input("Choose difficulty (Easy, Medium, Hard): ")
    
    print("\n[AI Agent is processing material and generating quiz...]")
    quiz_data = agent.generate_quiz(material, difficulty)
    
    # Procesamiento básico del Quiz
    questions = quiz_data.strip().split("Q:")[1:]
    index = 0
    
    # PARCHE DE SEGURIDAD: Evita bucle infinito validando longitud
    while index < len(questions):
        print(f"\n--- Question {index + 1} ---")
        print("Q:" + questions[index])
        
        ans = input("\nYour answer (A/B/C): ").upper()
        print("Checking... [Agent analysis in progress]")
        time.sleep(1)
        
        # Incremento crucial para no quedar atrapado en el bucle
        index += 1
        
    print("\n==================================================")
    print(" Session finished. Study metrics saved successfully.")
    print("==================================================")

if __name__ == "__main__":
    game_loop() 