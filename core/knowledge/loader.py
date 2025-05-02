from pathlib import Path
import json

class DocumentLoader:
    @staticmethod
    def load_from_json(path: str) -> dict:
        """Load documents from JSON file with validation"""
        file_path = Path(path)
        
        # Check if file exists and is not empty
        if not file_path.exists():
            raise FileNotFoundError(f"Document file not found: {path}")
        if file_path.stat().st_size == 0:
            return {}
            
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Invalid JSON in {path}, returning empty dict")
            return {}