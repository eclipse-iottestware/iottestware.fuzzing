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

from src.factory.abstract_builder import AbstractBuilder
from src.fuzzer.generator import RandomGenerator


class GeneratorBuilder(AbstractBuilder):

    def build_from_config(self, config):
        gen_conf = config.get('generators')
        gen_dict = dict()

        for i, g in enumerate(gen_conf):
            identifier = g.get('id')
            seed = g.get('seed', None)
            gen_dict.setdefault(identifier, RandomGenerator(identifier, seed))

        return gen_dict
