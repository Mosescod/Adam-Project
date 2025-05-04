def test_context_aware_search():
    mind = DivineKnowledge(quran_db)
    context = [{"question": "creation"}, {"question": "Adam"}]
    
    # Should prioritize verses mentioning both "mercy" AND creation/Adam
    verse = mind.search_verse("mercy", context=context)
    assert "creation" in verse or "Adam" in verse, "Context not boosting relevance"