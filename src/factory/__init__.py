# ********************************************************************************
# Copyright (c) 2019 Alexander Kaiser
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0.
#
# SPDX-License-Identifier: EPL-2.0
#
# Contributors:
#   Alexander Kaiser - initial API and implementation
# ********************************************************************************

import os
import sys
import json
import jsonschema
from jsonschema import Draft7Validator as Validator
from jsonschema import RefResolver
from collections import namedtuple

from src.factory.abstract_builder import BuilderException
from src.factory.protocol_module_builder import ProtocolModuleBuilder
from src.factory.rulesengine_builder import RulesEngineBuilder
from src.fuzzer.fuzzer import FuzzingEngine

from src.logger import get_factory_logger

factory_logger = get_factory_logger()

ROOT_SCHEMA_NAME = 'root.json'
ROOT_SCHEMA_DIR = os.path.dirname(os.path.abspath(os.path.join('resources', 'schema', ROOT_SCHEMA_NAME)))
ROOT_SCHEMA = os.path.join(ROOT_SCHEMA_DIR, ROOT_SCHEMA_NAME)
ROOT_SCHEMA_BASE_URI = 'file://' + ROOT_SCHEMA_DIR + '/'


def read_from_config_file(file_path):
    """
    build the configuration from a given file
    :param file_path:
    :return: the fuzzing proxy
    """
    try:
        with open(file_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError as fnfe:
        factory_logger.error(fnfe)
        sys.exit()
    except Exception as e:
        factory_logger.error(e)
        sys.exit()

    return config


def build_from_config(config):
    if isinstance(config, str):
        config = read_from_config_file(config)
    elif not isinstance(config, dict):
        factory_logger.error('Given configuration invalid: {}'.format(config))
        sys.exit()

    if not check_syntax(config, False):
        factory_logger.error('Syntax of given configuration invalid: {}'.format(config))
        sys.exit()

    pm_keyword = 'protocolModule'
    if pm_keyword not in config:
        factory_logger.error('Configuration does not have a {}: {}'.format(pm_keyword, config))
        sys.exit()

    pmb = ProtocolModuleBuilder()
    reb = RulesEngineBuilder()

    try:
        proto_module = pmb.build_from_config(config)
        rules_engine = reb.build_from_config(config)
    except (BuilderException, NotImplementedError) as e:
        factory_logger.error(e)
        sys.exit()

    fuzzing_engine = FuzzingEngine(rules_engine)

    # Note: technically this is the fuzzer containing of codec and the rules engine
    # TODO: ProtocolModule -> Codec
    # TODO: Merge FuzzingEngine and RulesEngine
    fuzzer = namedtuple('fuzzer', ['codec', 'fuzzing_engine'])
    return fuzzer(proto_module, fuzzing_engine)


def check_syntax(config, double_validate=True):
    """
    check the given configuration against the schema definition
    :param config:
    :param double_validate: validate invalid syntax a second time with raising exception
    :return: True if the syntax is valid, False otherwise
    """
    try:
        with open(ROOT_SCHEMA, 'r') as f:
            schema = json.load(f)
    except FileNotFoundError as fnfe:
        factory_logger.error('JSON root schema could not be found: {}'.format(ROOT_SCHEMA_NAME))
        factory_logger.error(fnfe)
        sys.exit()
    except Exception as e:
        factory_logger.error(e)
        sys.exit()

    # resolver: reference sub-schemas from relative URIs
    # -> https://github.com/Julian/jsonschema/issues/313
    resolver = RefResolver(base_uri=ROOT_SCHEMA_BASE_URI, referrer=schema)
    validator = Validator(schema, resolver=resolver)
    is_valid = validator.is_valid(config)

    if not is_valid and double_validate:
        # if configuration is invalid, run validate to get error message
        try:
            validator.validate(config)
        except jsonschema.exceptions.ValidationError as err:
            factory_logger.error(err)

    return is_valid
