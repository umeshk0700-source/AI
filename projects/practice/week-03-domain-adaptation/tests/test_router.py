from adapt.schemas import Requirement, Missing
from adapt.router import CapabilityRouter, CostModel

R = CapabilityRouter()


def _req(**kw):
    base = dict(description="x", missing=Missing.behaviour, knowledge_changes=False,
                knowledge_volume_tokens=2000, calls_per_month=5000, have_labeled_data=False)
    base.update(kw)
    return Requirement(**base)


def test_changing_knowledge_goes_to_rag():
    rec = R.recommend(_req(missing=Missing.knowledge, knowledge_changes=True))
    assert rec.approach == "rag"


def test_huge_corpus_goes_to_rag():
    rec = R.recommend(_req(missing=Missing.knowledge, knowledge_volume_tokens=500_000))
    assert rec.approach == "rag"


def test_behaviour_at_scale_goes_to_finetune():
    rec = R.recommend(_req(missing=Missing.behaviour, have_labeled_data=True,
                           calls_per_month=2_000_000))
    assert rec.approach == "finetune"
    assert set(rec.alternatives) == {"prompt", "rag"}


def test_default_is_prompt():
    assert R.recommend(_req()).approach == "prompt"


def test_cost_model_finetune_has_fixed_cost():
    r = _req(calls_per_month=0, knowledge_volume_tokens=0)
    assert CostModel.monthly("finetune", r) > CostModel.monthly("prompt", r)
    # at high volume, finetune's tiny context beats prompt's full context
    big = _req(calls_per_month=5_000_000, knowledge_volume_tokens=8000)
    assert CostModel.monthly("finetune", big) < CostModel.monthly("prompt", big)
