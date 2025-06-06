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

import postgresql.driver.dbapi20
from testing_support.db_settings import postgresql_settings
from testing_support.util import instance_hostname
from testing_support.validators.validate_database_trace_inputs import validate_database_trace_inputs
from testing_support.validators.validate_transaction_metrics import validate_transaction_metrics

from newrelic.api.background_task import background_task

DB_SETTINGS = postgresql_settings()[0]

_test_execute_via_cursor_scoped_metrics = [
    ("Function/postgresql.driver.dbapi20:connect", 1),
    ("Function/postgresql.driver.dbapi20:Connection.__enter__", 1),
    ("Function/postgresql.driver.dbapi20:Connection.__exit__", 1),
    (f"Datastore/statement/Postgres/{DB_SETTINGS['table_name']}/select", 1),
    (f"Datastore/statement/Postgres/{DB_SETTINGS['table_name']}/insert", 1),
    (f"Datastore/statement/Postgres/{DB_SETTINGS['table_name']}/update", 1),
    (f"Datastore/statement/Postgres/{DB_SETTINGS['table_name']}/delete", 1),
    ("Datastore/statement/Postgres/now/call", 1),
    ("Datastore/statement/Postgres/pg_sleep/call", 1),
    ("Datastore/operation/Postgres/drop", 1),
    ("Datastore/operation/Postgres/create", 1),
    ("Datastore/operation/Postgres/commit", 3),
    ("Datastore/operation/Postgres/rollback", 1),
    ("Datastore/operation/Postgres/other", 1),
]

_test_execute_via_cursor_rollup_metrics = [
    ("Datastore/all", 14),
    ("Datastore/allOther", 14),
    ("Datastore/Postgres/all", 14),
    ("Datastore/Postgres/allOther", 14),
    ("Datastore/operation/Postgres/select", 1),
    (f"Datastore/statement/Postgres/{DB_SETTINGS['table_name']}/select", 1),
    ("Datastore/operation/Postgres/insert", 1),
    (f"Datastore/statement/Postgres/{DB_SETTINGS['table_name']}/insert", 1),
    ("Datastore/operation/Postgres/update", 1),
    (f"Datastore/statement/Postgres/{DB_SETTINGS['table_name']}/update", 1),
    ("Datastore/operation/Postgres/delete", 1),
    (f"Datastore/statement/Postgres/{DB_SETTINGS['table_name']}/delete", 1),
    ("Datastore/operation/Postgres/drop", 1),
    ("Datastore/operation/Postgres/create", 1),
    ("Datastore/statement/Postgres/now/call", 1),
    ("Datastore/statement/Postgres/pg_sleep/call", 1),
    ("Datastore/operation/Postgres/call", 2),
    ("Datastore/operation/Postgres/commit", 3),
    ("Datastore/operation/Postgres/rollback", 1),
    ("Datastore/operation/Postgres/other", 1),
    (f"Datastore/instance/Postgres/{instance_hostname(DB_SETTINGS['host'])}/{DB_SETTINGS['port']}", 13),
    ("Function/postgresql.driver.dbapi20:connect", 1),
    ("Function/postgresql.driver.dbapi20:Connection.__enter__", 1),
    ("Function/postgresql.driver.dbapi20:Connection.__exit__", 1),
]


@validate_transaction_metrics(
    "test_database:test_execute_via_cursor",
    scoped_metrics=_test_execute_via_cursor_scoped_metrics,
    rollup_metrics=_test_execute_via_cursor_rollup_metrics,
    background_task=True,
)
@validate_database_trace_inputs(sql_parameters_type=tuple)
@background_task()
def test_execute_via_cursor():
    with postgresql.driver.dbapi20.connect(
        database=DB_SETTINGS["name"],
        user=DB_SETTINGS["user"],
        password=DB_SETTINGS["password"],
        host=DB_SETTINGS["host"],
        port=DB_SETTINGS["port"],
    ) as connection:
        cursor = connection.cursor()

        cursor.execute(f"""drop table if exists {DB_SETTINGS["table_name"]}""")

        cursor.execute(f"create table {DB_SETTINGS['table_name']} (a integer, b real, c text)")

        cursor.executemany(
            f"insert into {DB_SETTINGS['table_name']} values (%s, %s, %s)",
            [(1, 1.0, "1.0"), (2, 2.2, "2.2"), (3, 3.3, "3.3")],
        )

        cursor.execute(f"""select * from {DB_SETTINGS["table_name"]}""")

        cursor.execute(
            f"with temporaryTable (averageValue) as (select avg(b) from {DB_SETTINGS['table_name']}) select * from {DB_SETTINGS['table_name']},temporaryTable where {DB_SETTINGS['table_name']}.b > temporaryTable.averageValue"
        )

        cursor.execute(f"update {DB_SETTINGS['table_name']} set a=%s, b=%s, c=%s where a=%s", (4, 4.0, "4.0", 1))

        cursor.execute(f"""delete from {DB_SETTINGS["table_name"]} where a=2""")

        connection.commit()

        cursor.callproc("now", ())
        cursor.callproc("pg_sleep", (0.25,))

        connection.rollback()
        connection.commit()


_test_rollback_on_exception_scoped_metrics = [
    ("Function/postgresql.driver.dbapi20:connect", 1),
    ("Function/postgresql.driver.dbapi20:Connection.__enter__", 1),
    ("Function/postgresql.driver.dbapi20:Connection.__exit__", 1),
    ("Datastore/operation/Postgres/rollback", 1),
]

_test_rollback_on_exception_rollup_metrics = [
    ("Datastore/all", 2),
    ("Datastore/allOther", 2),
    ("Datastore/Postgres/all", 2),
    ("Datastore/Postgres/allOther", 2),
]


@validate_transaction_metrics(
    "test_database:test_rollback_on_exception",
    scoped_metrics=_test_rollback_on_exception_scoped_metrics,
    rollup_metrics=_test_rollback_on_exception_rollup_metrics,
    background_task=True,
)
@validate_database_trace_inputs(sql_parameters_type=tuple)
@background_task()
def test_rollback_on_exception():
    try:
        with postgresql.driver.dbapi20.connect(
            database=DB_SETTINGS["name"],
            user=DB_SETTINGS["user"],
            password=DB_SETTINGS["password"],
            host=DB_SETTINGS["host"],
            port=DB_SETTINGS["port"],
        ):
            raise RuntimeError("error")

    except RuntimeError:
        pass
