# Copyright 2010 New Relic, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from pathlib import Path

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

collector_agent_registration = collector_agent_registration_fixture(
    app_name="Python Agent Test (agent_benchmarks)", default_settings=_default_settings
)


class _DeveloperModeBenchmark:
    def setup(self):
        # Register the agent with the collector using the pytest fixture manually
        self._collector_agent_registration = collector_agent_registration()
        self.application = application = next(self._collector_agent_registration)

        # Wait for the application to become active.
        collector_available_fixture(application)

    def teardown(self):
        # Teardown the pytest fixture manually
        try:
            next(self._collector_agent_registration)
        except StopIteration:
            pass
