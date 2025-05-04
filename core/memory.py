from datetime import datetime
import json
from pathlib import Path

class ConversationMemory:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.file_path = f"conversations/{user_id}.json"
        self._setup_storage()
        self.context_window = [] 
        
    def _setup_storage(self):
        """Create file if nonexistent"""
        Path(self.file_path).parent.mkdir(exist_ok=True)
        if not Path(self.file_path).exists():
            with open(self.file_path, 'w') as f:
                json.dump([], f)
    
    def get_context(self) -> list:
        """Get recent conversation context"""
        return self.context_window[-3:]
        
    def store(self, question: str, response: str):
        """Archive with context tracking"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'question': question,
            'response': response
        }
        self.context_window.append(entry)
        if len(self.context_window) > 3:
            self.context_window.pop(0)