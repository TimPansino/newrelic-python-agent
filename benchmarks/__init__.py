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

from newrelic.common.object_wrapper import function_wrapper

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

BENCHMARK_PREFIXES = ("time", "mem")


def setup_collector_agent_registration(instance):
    # Register the agent with the collector using the pytest fixture manually
    instance._collector_agent_registration = collector_agent_registration()
    instance.application = application = next(instance._collector_agent_registration)

    # Wait for the application to become active.
    collector_available_fixture(application)


def teardown_collector_agent_registration(instance):
    # Teardown the pytest fixture manually
    try:
        next(instance._collector_agent_registration)
    except StopIteration:
        pass


@function_wrapper
def wrap_benchmark_method(wrapped, instance, args, kwargs):
    wrapped(*args, **kwargs)  # Run the benchmark
    return 0  # Return the number of bytes produced by the agent during this benchmark here


def benchmark(cls):
    # Find all methods not prefixed with underscores and treat them as benchmark methods
    benchmark_methods = {
        name: method for name, method in vars(cls).items() if callable(method) and not name.startswith("_")
    }

    # Remove setup and teardown functions from benchmark methods and save them
    cls._setup = benchmark_methods.pop("setup", None)
    cls._teardown = benchmark_methods.pop("teardown", None)

    # Patch in benchmark methods for each prefix
    for name, method in benchmark_methods.items():
        for prefix in BENCHMARK_PREFIXES:
            if prefix == "track":
                # Wrap track_ methods in a wrapper that returns the bytes produced by the agent during this benchmark
                setattr(cls, f"{prefix}_{name}", wrap_benchmark_method(method))
            else:
                setattr(cls, f"{prefix}_{name}", method)

    # Define agent activation as setup and teardown functions
    def setup(self):
        setup_collector_agent_registration(self)

        # Call the original setup if it exists
        if getattr(self, "_setup", None) is not None:
            self._setup()

    def teardown(self):
        teardown_collector_agent_registration(self)

        # Call the original teardown if it exists
        if getattr(self, "_teardown", None) is not None:
            self._teardown()

    # Patch in new setup and teardown methods
    cls.setup = setup
    cls.teardown = teardown

    return cls
