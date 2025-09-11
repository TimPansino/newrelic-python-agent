import sys
from pathlib import Path
from threading import Lock

# Amend sys.path to allow importing fixtures from testing_support
tests_path = Path(__file__).parent.parent / "tests"
sys.path.append(str(tests_path))

from testing_support.fixtures import collector_agent_registration_fixture, collector_available_fixture  # noqa: E402

_default_settings = {
    "package_reporting.enabled": False,  # Turn off package reporting for testing as it causes slow downs.
    "transaction_tracer.explain_threshold": 0.0,
    "transaction_tracer.transaction_threshold": 0.0,
    "transaction_tracer.stack_trace_threshold": 0.0,
    "debug.log_data_collector_payloads": True,
    "debug.record_transaction_failure": True,
}

_collector_agent_registration_fixture = collector_agent_registration_fixture(
    app_name="Python Agent Test (benchmarks)", default_settings=_default_settings
)

INITIALIZATION_LOCK = Lock()
APPLICATIONS = []
FIXTURES = []


def collector_agent_registration(instance):
    # If the application is already registered, exit early
    if APPLICATIONS:
        return

    # Register the agent with the collector using the pytest fixture manually
    with INITIALIZATION_LOCK:
        fixture = _collector_agent_registration_fixture()
        FIXTURES.append(fixture)
        APPLICATIONS.append(next(fixture))
        instance.application = APPLICATIONS[0]

        # Wait for the application to become active
        collector_available_fixture(APPLICATIONS[0])
