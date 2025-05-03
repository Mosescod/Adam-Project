# Test the analyzer
from core.knowledge.analyzer import MindAnalyzer
print(MindAnalyzer().detect_themes("Who created Adam from clay?"))
# Should output: ['creation']