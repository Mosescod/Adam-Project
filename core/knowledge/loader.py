from pathlib import Path
import json

class DocumentLoader:
    @staticmethod
    def load_from_json(path: str) -> dict:
        """Load documents with validation"""
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"Document file not found at {file_path}")
        if file_path.stat().st_size == 0:
            return {}
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    raise ValueError("Document data should be a dictionary")
                return data
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in {file_path}")