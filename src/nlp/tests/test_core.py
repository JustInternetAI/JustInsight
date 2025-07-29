from nlp.core import run_ner_hf

def test_run_ner_hf():
    sample_text = "Grace Madison hates the Mariners."
    entities = run_ner_hf(sample_text)
    assert isinstance(entities, list)
    assert any(ent['entity_group'] == 'PER' for ent in entities)  # Example check that a person entity is found
