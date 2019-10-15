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

from src.factory.abstract_builder import AbstractBuilder, BuilderException
from src.fuzzer.mutator import MutatorType, BinaryOperationMutator, UnaryOperationMutator
from src.fuzzer.operators import BinaryOperation, UnaryOperation
from src.factory.generator_builder import GeneratorBuilder
from src.fuzzer.generator import FixedGenerator, AbstractGenerator


class MutatorBuilder(AbstractBuilder):
    """
    MutatorBuilder simplifies the creation of a 'Simple'Mutator
    #1 creation of objects is separated from operational interface
    #2 MutatorBuilder.build() ensures that the mutator is complete and correct,
       no checks during runtime required
    """
    _identifier = None
    _field = None
    _generator = None
    _operator_type = None

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, value: str):
        self._identifier = value

    @property
    def field(self):
        return self._field

    @field.setter
    def field(self, value: str):
        self._field = value

    @property
    def operator_type(self):
        return self._operator_type

    @operator_type.setter
    def operator_type(self, value: MutatorType):
        self._operator_type = value

    @property
    def generator(self):
        return self._generator

    @generator.setter
    def generator(self, value: AbstractGenerator):
        self._generator = value

    def build_from_config(self, config):
        mutators_dict = dict()
        mutators_conf = config.get('mutators')

        gb = GeneratorBuilder()
        generators_dict = gb.build_from_config(config)

        for m in mutators_conf:
            identifier = m.get('id')

            if 'binary' in m:
                operator = BinaryOperation.from_string(m.get('binary'))
                mutator = BinaryOperationMutator(identifier, operator)
            elif 'unary' in m:
                operator = UnaryOperation.from_string(m.get('unary'))
                mutator = UnaryOperationMutator(identifier, operator)
            else:
                raise BuilderException('Mutator configuration "{}" not supported'.format(m))

            if 'field' in m:
                mutator.field = m.get('field')
            else:
                raise BuilderException('Mutator "{}" does not contain a field'.format(identifier))

            if 'generator' in m:
                generator_id = m.get('generator')
                try:
                    mutator.generator = generators_dict[generator_id]
                except KeyError:
                    raise BuilderException('Mutator "{}" references generator "{}" which is undefined'
                                           .format(identifier, generator_id))
            elif 'hex' in m:
                value = m.get('hex')
                mutator.generator = FixedGenerator(value)  # FixedValueGenerator is not predefined in generators_dict

            if identifier not in mutators_dict:
                mutators_dict[identifier] = mutator
            else:
                raise BuilderException('Duplicate Mutator ID "{}"'.format(identifier))

        return mutators_dict
