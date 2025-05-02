from core.personality import AdamPersonality
from core.knowledge.synthesizer import KnowledgeSynthesizer
from core.memory import ConversationMemory

class AdamCLI:
    def __init__(self):
        self.personality = AdamPersonality()
        self.knowledge = KnowledgeSynthesizer()
        self.memory = ConversationMemory("default_user")
        
    def run(self):
        print("Adam: *molding clay* Speak, and I shall answer in the name of my Lord.")
        while True:
            try:
                question = input("\nYou: ").strip()
                if question.lower() in ['exit', 'quit']:
                    print("\nAdam: Peace be upon thee until we meet again.")
                    break
                
                # Generate response
                islamic_answer = self.knowledge.query(question)
                response = (self.personality.respond(islamic_answer) 
                           if islamic_answer 
                           else "I must consult the Scriptures further.")
                
                print(f"\nAdam: {response}")
                self.memory.store(question, response)
                
            except KeyboardInterrupt:
                print("\nAdam: *brushing dust from hands* The angel calls me away.")
                break