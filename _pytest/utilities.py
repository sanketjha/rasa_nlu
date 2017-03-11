import tempfile

from rasa_nlu import pipeline
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.data_router import DataRouter
from rasa_nlu.train import do_train


def base_test_conf(pipeline_name):
    return RasaNLUConfig(cmdline_args={
        'response_log': temp_log_file_dir(),
        'port': 5022,
        "pipeline": pipeline.registered_pipelines[pipeline_name],
        "path": tempfile.mkdtemp(),
        "data": "./data/examples/rasa/demo-rasa.json"
    })


def interpreter_for(interpreter_builder, config):
    (trained, path) = run_train(config)
    interpreter = load_interpreter_for_model(config, path, interpreter_builder)
    return interpreter


def temp_log_file_dir():
    return tempfile.mkdtemp(suffix="_rasa_nlu_logs")


def run_train(config):
    (trained, path) = do_train(config)
    return trained, path


def load_interpreter_for_model(config, persisted_path, interpreter_builder):
    metadata = DataRouter.read_model_metadata(persisted_path, config)
    return interpreter_builder.create_interpreter(metadata, config)


class ResponseTest(object):
    def __init__(self, endpoint, expected_response, payload=None):
        self.endpoint = endpoint
        self.expected_response = expected_response
        self.payload = payload
