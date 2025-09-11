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

from newrelic.agent import background_task, current_transaction

from . import benchmark


@benchmark
class NRActiveSuite:
    def nr_active(self):
        from newrelic.agent import application

        assert application().active, "Application not active!"

    @background_task()
    def active_transaction(self):
        assert current_transaction(), "No active transaction!"


# TODO REMOVE THIS - DOING SIMPLE SCALING LOAD TESTING WITH THIS
for i in range(1, 100):
    globals()[f"NRActiveSuite_{i}"] = type(f"NRActiveSuite_{i}", (NRActiveSuite,), {})
