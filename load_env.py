import json
import os

valid_envs = ["develop", "staging", "prod"]


def get_valid_envs():
    return valid_envs


def load_environment_variables(parent_level: int = 0):
    path_to_import = os.getcwd()
    for level in range(0, parent_level):
        path_to_import = os.path.join(path_to_import, os.pardir)

    with open(os.path.join(os.path.abspath(path_to_import), f'env.json')) as json_file:
        variables = json.load(json_file)

    for key in variables:
        os.environ[key] = variables[key]
