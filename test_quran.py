from core.knowledge.quran import QuranAPI
import time

def test_quran_api():
    print("\n🔍 Testing Enhanced Quran API...")
    quran = QuranAPI()
    
    # Test 1: First call (API)
    start = time.time()
    verse = quran.search_ayah("mercy")
    print(f"\nTest 1 - First call (API):\n{verse or 'No verse found'}")
    print(f"Time taken: {time.time() - start:.2f}s")
    
    # Test 2: Cached call
    start = time.time()
    verse = quran.search_ayah("mercy")
    print(f"\nTest 2 - Cached call:\n{verse or 'No verse found'}")
    print(f"Time taken: {time.time() - start:.2f}s")

if __name__ == "__main__":
    test_quran_api()