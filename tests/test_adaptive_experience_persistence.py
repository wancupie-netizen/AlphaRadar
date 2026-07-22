"""
Tests for Adaptive Experience persistence contracts.
"""

from datetime import datetime, timezone
from unittest.mock import Mock, patch

import pytest

from adaptive.artifacts.experience_artifact import (
    ExperienceArtifact,
    ExperienceMetadata,
)

from adaptive.deserializers.experience_deserializer import (
    deserialize_experience,
)

from adaptive.serializers.experience_serializer import (
    serialize_experience,
)

from scanner.adaptive_experience_store import (
    load_experience_payloads,
    save_experience_payload,
)


# ==========================================================
# Fixture
# ==========================================================

def build_experience() -> ExperienceArtifact:
    """
    Build a reusable ExperienceArtifact.
    """

    return ExperienceArtifact(

        experience_id=
            "EXP-TEST123",

        fingerprint=
            "BTC-FINGERPRINT",

        sample_size=
            1,

        success_count=
            1,

        failure_count=
            0,

        success_rate=
            100.0,

        last_seen=
            datetime(
                2026,
                7,
                22,
                10,
                30,
                tzinfo=timezone.utc,
            ),

        metadata=
            ExperienceMetadata(

                engine_version=
                    "1.0.0",

                timestamp=
                    datetime(
                        2026,
                        7,
                        22,
                        10,
                        31,
                        tzinfo=timezone.utc,
                    ),

            ),

    )


# ==========================================================
# Serialization
# ==========================================================

def test_should_serialize_experience():
    """
    Serializer should preserve every persistence field.
    """

    experience = build_experience()

    payload = serialize_experience(
        experience,
    )

    assert payload == {

        "experience_id":
            "EXP-TEST123",

        "fingerprint":
            "BTC-FINGERPRINT",

        "sample_size":
            1,

        "success_count":
            1,

        "failure_count":
            0,

        "success_rate":
            100.0,

        "last_seen":
            "2026-07-22T10:30:00+00:00",

        "engine_version":
            "1.0.0",

        "artifact_timestamp":
            "2026-07-22T10:31:00+00:00",

    }


def test_should_reject_missing_experience():
    """
    Serializer should reject missing artifacts.
    """

    with pytest.raises(
        ValueError,
        match="ExperienceArtifact is required",
    ):

        serialize_experience(
            None,
        )


# ==========================================================
# Deserialization
# ==========================================================

def test_should_deserialize_experience():
    """
    Deserializer should preserve original artifact identity.
    """

    original = build_experience()

    payload = serialize_experience(
        original,
    )

    restored = deserialize_experience(
        payload,
    )

    assert restored == original

    assert restored.experience_id == (
        "EXP-TEST123"
    )


def test_should_reject_incomplete_payload():
    """
    Missing required fields should fail clearly.
    """

    with pytest.raises(
        ValueError,
        match="Experience payload is missing",
    ):

        deserialize_experience(
            {
                "experience_id":
                    "EXP-INCOMPLETE",
            }
        )


# ==========================================================
# Store
# ==========================================================

@patch(
    "scanner.adaptive_experience_store.supabase"
)
def test_should_save_experience_payload(
    mock_supabase,
):
    """
    Store should insert serialized Experience payload.
    """

    payload = serialize_experience(
        build_experience(),
    )

    table = Mock()
    insert = Mock()

    mock_supabase.table.return_value = table

    table.insert.return_value = insert

    save_experience_payload(
        payload,
    )

    mock_supabase.table.assert_called_once_with(
        "adaptive_experiences",
    )

    table.insert.assert_called_once_with(
        payload,
    )

    insert.execute.assert_called_once_with()


@patch(
    "scanner.adaptive_experience_store.supabase"
)
def test_should_load_experience_payloads(
    mock_supabase,
):
    """
    Store should retrieve history in chronological order.
    """

    payload = serialize_experience(
        build_experience(),
    )

    response = Mock()
    response.data = [
        payload,
    ]

    table = Mock()
    select = Mock()
    equal = Mock()
    ordered = Mock()

    mock_supabase.table.return_value = table

    table.select.return_value = select

    select.eq.return_value = equal

    equal.order.return_value = ordered

    ordered.execute.return_value = response

    result = load_experience_payloads(
        "BTC-FINGERPRINT",
    )

    assert result == [
        payload,
    ]

    mock_supabase.table.assert_called_once_with(
        "adaptive_experiences",
    )

    select.eq.assert_called_once_with(

        "fingerprint",

        "BTC-FINGERPRINT",

    )

    equal.order.assert_called_once_with(

        "last_seen",

        desc=False,

    )


def test_should_reject_empty_fingerprint():
    """
    Store should reject empty fingerprint queries.
    """

    with pytest.raises(
        ValueError,
        match="Knowledge Fingerprint is required",
    ):

        load_experience_payloads(
            "   ",
        )