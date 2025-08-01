from nlp.core import run_ner_hf
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

def test_run_ner_hf():
    sample_text = "Grace Madison hates the Mariners."
    entities = run_ner_hf(sample_text)

    print("Entities:", entities)

    assert isinstance(entities, list)
    assert all(isinstance(ent, dict) for ent in entities)

    for ent in entities:
        print("Entity keys:", ent.keys())

    assert any(ent.get("entity_group") == 'PER' for ent in entities)  # Example check that a person entity is found
