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

import pymemcache.client
from testing_support.db_settings import memcached_settings
from testing_support.validators.validate_transaction_metrics import validate_transaction_metrics

from newrelic.api.background_task import background_task
from newrelic.api.transaction import set_background_task
from newrelic.common import system_info

DB_SETTINGS = memcached_settings()[0]

MEMCACHED_HOST = DB_SETTINGS["host"]
MEMCACHED_PORT = DB_SETTINGS["port"]
MEMCACHED_NAMESPACE = DB_SETTINGS["namespace"]
MEMCACHED_ADDR = (MEMCACHED_HOST, int(MEMCACHED_PORT))
INSTANCE_METRIC_HOST = system_info.gethostname() if MEMCACHED_HOST == "127.0.0.1" else MEMCACHED_HOST
INSTANCE_METRIC_NAME = f"Datastore/instance/Memcached/{INSTANCE_METRIC_HOST}/{MEMCACHED_PORT}"


_test_bt_set_get_delete_scoped_metrics = [
    ("Datastore/operation/Memcached/set", 1),
    ("Datastore/operation/Memcached/get", 1),
    ("Datastore/operation/Memcached/delete", 1),
]

_test_bt_set_get_delete_rollup_metrics = [
    ("Datastore/all", 3),
    ("Datastore/allOther", 3),
    ("Datastore/Memcached/all", 3),
    ("Datastore/Memcached/allOther", 3),
    ("Datastore/operation/Memcached/set", 1),
    ("Datastore/operation/Memcached/get", 1),
    ("Datastore/operation/Memcached/delete", 1),
    (INSTANCE_METRIC_NAME, 3),
]


@validate_transaction_metrics(
    "test_memcache:test_bt_set_get_delete",
    scoped_metrics=_test_bt_set_get_delete_scoped_metrics,
    rollup_metrics=_test_bt_set_get_delete_rollup_metrics,
    background_task=True,
)
@background_task()
def test_bt_set_get_delete():
    set_background_task(True)
    client = pymemcache.client.Client(MEMCACHED_ADDR)

    key = f"{MEMCACHED_NAMESPACE}key"

    client.set(key, b"value")
    value = client.get(key)
    client.delete(key)

    assert value == b"value"


_test_wt_set_get_delete_scoped_metrics = [
    ("Datastore/operation/Memcached/set", 1),
    ("Datastore/operation/Memcached/get", 1),
    ("Datastore/operation/Memcached/delete", 1),
]

_test_wt_set_get_delete_rollup_metrics = [
    ("Datastore/all", 3),
    ("Datastore/allWeb", 3),
    ("Datastore/Memcached/all", 3),
    ("Datastore/Memcached/allWeb", 3),
    ("Datastore/operation/Memcached/set", 1),
    ("Datastore/operation/Memcached/get", 1),
    ("Datastore/operation/Memcached/delete", 1),
    (INSTANCE_METRIC_NAME, 3),
]


@validate_transaction_metrics(
    "test_memcache:test_wt_set_get_delete",
    scoped_metrics=_test_wt_set_get_delete_scoped_metrics,
    rollup_metrics=_test_wt_set_get_delete_rollup_metrics,
    background_task=False,
)
@background_task()
def test_wt_set_get_delete():
    set_background_task(False)
    client = pymemcache.client.Client(MEMCACHED_ADDR)

    key = f"{MEMCACHED_NAMESPACE}key"

    client.set(key, b"value")
    value = client.get(key)
    client.delete(key)

    assert value == b"value"
