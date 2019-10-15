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
from src.factory.mutator_builder import MutatorBuilder
from src.factory.matching_filter_builder import MatchingFilterBuilder
from src.fuzzer.distribution import Multinomial
from src.fuzzer.rulesengine import RulesEngine, Rule, FuzzyRule
from src.factory.abstract_builder import AbstractBuilder, BuilderException


class RulesEngineBuilder(AbstractBuilder):

    _filters_dict = None
    _mutators_dict = None
    _rules_engine = None

    @property
    def filters_dict(self):
        return self._filters_dict

    @filters_dict.setter
    def filters_dict(self, value):
        self._filters_dict = value

    @property
    def mutators_dict(self):
        return self._mutators_dict

    @mutators_dict.setter
    def mutators_dict(self, value):
        self._mutators_dict = value

    @property
    def rules_engine(self):
        return self._rules_engine

    def build_from_config(self, config):
        rules_conf = config.get('rules')
        rules = []

        mb = MutatorBuilder()
        self._mutators_dict = mb.build_from_config(config)

        mfb = MatchingFilterBuilder()
        self._filters_dict = mfb.build_from_config(config)

        for i, r in enumerate(rules_conf):
            match_filter_id = r.get('match')

            if match_filter_id in self._filters_dict:
                match_filter = self._filters_dict[match_filter_id]
            else:
                raise BuilderException('Rule "{}" references undefined matching filter "{}"'.format(i, match_filter_id))

            rule_id = match_filter_id

            if 'mutators' in r:
                mutator_ids = r.get('mutators')
                rule = self.__build_mutators_only(i, rule_id, match_filter, mutator_ids)
                rules.append(rule)
            elif 'distribution' in r:
                d_conf = r.get('distribution')
                rule = self.__build_mutators_distribution(i, rule_id, match_filter, d_conf)
                rules.append(rule)
            else:
                raise BuilderException('Rule "{}" does not reference any mutators'.format(i))

        self._rules_engine = RulesEngine(rules)
        return self._rules_engine

    def build(self):
        if self._rules_engine:
            return self._rules_engine
        else:
            raise BuilderException('No rules generated!')

    def __build_mutators_only(self, rule_idx, rule_id, match_filter, mutator_ids):
        mutators = self.__get_mutators_by_ids(rule_id, mutator_ids)
        rule = Rule(rule_idx, rule_id, match_filter, mutators)
        return rule

    def __build_mutators_distribution(self, rule_idx, rule_id, match_filter, distribution_conf):
        # model = distribution_conf.get('model')  # TODO: use the model once other distribution models are implemented
        seed = distribution_conf.get('seed', None)

        # num of experiments defaults to 3 if not given
        # see. https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.random.multinomial.html
        nxp = distribution_conf.get('nxp', 3)

        mutators_list = []
        strengths = []
        for item in distribution_conf.get('items'):
            strength = item.get('strength')
            mutator_ids = item.get('mutators')
            mutators = self.__get_mutators_by_ids(rule_id, mutator_ids)

            strengths.append(strength)
            mutators_list.append(mutators)

        distribution = Multinomial(strengths, nxp, seed)
        rule = FuzzyRule(rule_idx, rule_id, match_filter, mutators_list, distribution)
        return rule

    def __get_mutators_by_ids(self, rule_id, mutator_ids):
        mutators = []
        for m in mutator_ids:
            if m in self._mutators_dict:
                mutators.append(self._mutators_dict[m])
            else:
                raise BuilderException('Rule "{}" references undefined mutator "{}"'.format(rule_id, m))

        return mutators
