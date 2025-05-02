from core.personality import AdamPersonality
from core.adam_rules import respond
from core.knowledge.synthesizer import DocumentSynthesizer  # Your existing RAG system
from core.knowledge.loader import DocumentLoader
import signal
import sys

class AdamAI:
    def __init__(self):
        print("Initializing First Human Adam...")
        self.documents = DocumentLoader.load_from_json("core/knowledge/data/documents.json")
        self.synthesizer = DocumentSynthesizer(self.documents)  # Your existing setup
        self.personality = AdamPersonality("User", self.synthesizer)

    def query(self, question: str) -> str:
        # 1. Check for Islamic keywords
        islamic_terms = ['allah', 'quran', 'surah', 'prophet', 'prayer']
        if any(term in question.lower() for term in islamic_terms):
            quran_result = self.quran_api.get_ayah(question)
            if quran_result:
                return self.personality._quranic_response(question, quran_result)
            
        # 2. Fallback to adam rules
        return respond(question)

    def run(self):
        print("\nAdam: *brushes clay from hands* Speak, and I will answer.")
        while True:
            try:
                question = input("\nYou: ").strip()
                if question.lower() in ['exit', 'quit']:
                    print("\nAdam: *nods* Until the next sunrise.")
                    break
                    
                response = self.query(question)
                print(f"\nAdam: {response}")
                
            except KeyboardInterrupt:
                print("\nAdam: *tilts head* The wind calls me away.")
                break

    def show_personality(self):
        """ASCII art trait display"""
        print("\nAdam's Current State:")
        for trait, value in self.personality.traits.items():
            bar = '▓' * int(value * 20) + '░' * (20 - int(value * 20))
            print(f"{trait.upper():<18} {bar} {value:.2f}")

if __name__ == "__main__":
    ai = AdamAI()
    ai.run()