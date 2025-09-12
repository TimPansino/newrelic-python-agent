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
    def bench_application(self):
        from newrelic.agent import application

        assert application()

    def bench_application_active(self):
        from newrelic.agent import application

        assert application().active

    @background_task()
    def bench_background_task(self):
        assert current_transaction()


# accept_distributed_trace_headers
# accept_distributed_trace_payload
# add_custom_attribute
# add_custom_attributes
# add_custom_parameter
# add_custom_parameters
# add_custom_span_attribute
# add_framework_info
# application
# application_settings
# asgi_application
# background_task
# callable_name
# capture_request_params
# create_distributed_trace_payload
# current_span_id
# current_trace
# current_trace_id
# current_transaction
# data_source_factory
# data_source_generator
# database_trace
# datastore_trace
# disable_browser_autorum
# end_of_transaction
# error_trace
# external_trace
# extra_settings
# function_trace
# function_wrapper
# generator_trace
# get_browser_timing_footer
# get_browser_timing_header
# get_linking_metadata
# global_settings
# ignore_transaction
# in_function
# initialize
# insert_distributed_trace_headers
# insert_html_snippet
# lambda_handler
# message_trace
# message_transaction
# notice_error
# out_function
# patch_function_wrapper
# post_function
# pre_function
# profile_trace
# record_custom_event
# record_custom_metric
# record_custom_metrics
# record_exception
# record_llm_feedback_event
# record_log_event
# record_ml_event
# register_application
# register_data_source
# register_database_client
# resolve_path
# set_background_task
# set_error_group_callback
# set_llm_token_count_callback
# set_transaction_name
# set_user_id
# shutdown_agent
# suppress_apdex_metric
# suppress_transaction_trace
# transaction_name
# transient_function_wrapper
# verify_body_exists
# web_transaction
# wrap_asgi_application
# wrap_background_task
# wrap_database_trace
# wrap_datastore_trace
# wrap_error_trace
# wrap_external_trace
# wrap_function_trace
# wrap_function_wrapper
# wrap_generator_trace
# wrap_in_function
# wrap_message_trace
# wrap_message_transaction
# wrap_mlmodel
# wrap_object
# wrap_object_attribute
# wrap_out_function
# wrap_post_function
# wrap_pre_function
# wrap_profile_trace
# wrap_transaction_name
# wrap_web_transaction
# wrap_wsgi_application
# wsgi_application


# TODO REMOVE THIS - DOING SIMPLE SCALING LOAD TESTING WITH THIS
# for i in range(1, 100):
#     globals()[f"NRActiveSuite_{i:02d}"] = type(f"NRActiveSuite_{i:02d}", (NRActiveSuite,), {})
