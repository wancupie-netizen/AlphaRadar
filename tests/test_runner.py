"""
Tests for AlphaRadar Runner.
"""

from unittest.mock import patch

from scanner.runner import run_scan


@patch("scanner.runner.finish_job")
@patch("scanner.runner.start_job")
@patch("scanner.runner.load_latest_intelligence")
@patch("scanner.runner.save_intelligence")
@patch("scanner.runner.should_store")
@patch("scanner.runner.build_intelligence")
@patch("scanner.runner.build_observation")
@patch("scanner.runner.save_market_event")
@patch("scanner.runner.normalize_pair")
@patch("scanner.runner.select_best_pair")
@patch("scanner.runner.search_token")
def test_should_complete_successful_scan(

    mock_search,
    mock_select_pair,
    mock_normalize,
    mock_save_event,
    mock_build_observation,
    mock_build_intelligence,
    mock_should_store,
    mock_save_intelligence,
    mock_load_latest,
    mock_start_job,
    mock_finish_job,

):

    mock_start_job.return_value = "JOB"

    mock_finish_job.return_value = 123

    mock_search.return_value = {
        "pairs": [
            {
                "pairAddress": "ABC"
            }
        ]
    }

    mock_select_pair.return_value = {
        "pairAddress": "ABC"
    }

    event = {
        "token": "BTC"
    }

    observation = {
        "token": "BTC"
    }

    package = {
        "token": "BTC",
        "observation": observation,
        "signals": [],
        "interpretations": [],
        "decision": {},
    }

    mock_normalize.return_value = event
    mock_build_observation.return_value = observation
    mock_build_intelligence.return_value = package

    mock_load_latest.return_value = None

    mock_should_store.return_value = True

    result = run_scan("BTC")

    assert result["success"] is True
    assert result["knowledge_saved"] is True

    mock_search.assert_called_once_with("BTC")

    mock_select_pair.assert_called_once()

    mock_normalize.assert_called_once()

    mock_save_event.assert_called_once_with(event)

    mock_build_observation.assert_called_once_with("BTC")

    mock_build_intelligence.assert_called_once_with(
        "BTC",
        observation,
    )

    mock_should_store.assert_called_once_with(
        package,
        None,
    )

    mock_save_intelligence.assert_called_once_with(
        package,
    )

    mock_finish_job.assert_called()