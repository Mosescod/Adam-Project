from datetime import datetime
import json

class ConversationMemory:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.file_path = f"conversations/{user_id}.json"
        self._setup_storage()
        
    def _setup_storage(self):
        """Create file if nonexistent"""
        Path(self.file_path).parent.mkdir(exist_ok=True)
        if not Path(self.file_path).exists():
            with open(self.file_path, 'w') as f:
                json.dump([], f)
    
    def store(self, question: str, response: str):
        """Archive conversations with timestamps"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'question': question,
            'response': response
        }
        with open(self.file_path, 'r+') as f:
            data = json.load(f)
            data.append(entry)
            f.seek(0)
            json.dump(data, f)