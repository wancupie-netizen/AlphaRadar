from adaptive.identity.decision_id import generate_decision_id


def test_generate_decision_id_returns_string():

    decision_id = generate_decision_id()

    assert isinstance(decision_id, str)


def test_generate_decision_id_is_not_empty():

    decision_id = generate_decision_id()

    assert decision_id != ""


def test_generate_decision_id_is_unique():

    id1 = generate_decision_id()
    id2 = generate_decision_id()

    assert id1 != id2