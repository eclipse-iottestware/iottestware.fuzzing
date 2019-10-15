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
from src.factory.abstract_builder import AbstractBuilder, IncompleteFilterException
from src.fuzzer.filter import SimpleFilter, ComplexFilter, FilterDirection


class MatchingFilterBuilder(AbstractBuilder):

    def build_from_config(self, config):
        filters_conf = config.get('filters')
        matching_filters_dict = dict()

        for i, matching_filter in enumerate(filters_conf):
            identifier = matching_filter.get('id')

            if 'filter' in matching_filter:
                filter = self.__simple_filter(identifier, matching_filter.get('filter'))
            elif 'left' in matching_filter:
                left = matching_filter.get('left')
                right = matching_filter.get('right')
                op = matching_filter.get('op')
                filter = self.__complex_filter(identifier, left, right, op)
            else:
                raise NotImplementedError('Filter: {}'.format(matching_filter))

            # look if filter description is given
            filter.description = matching_filter.get('description', None)

            # look for the direction
            direction = matching_filter.get('direction', 'All')  # default All
            if direction == 'Request':
                filter.filter_direction = FilterDirection.REQUEST
            elif direction == 'Response':
                filter.filter_direction = FilterDirection.RESPONSE
            else:
                filter.filter_direction = FilterDirection.ALL

            matching_filters_dict[identifier] = filter

        return matching_filters_dict

    def __complex_filter(self, identifier, filter_conf_left, filter_conf_right, operator):
        branches = [filter_conf_left, filter_conf_right]
        filter_objects = []

        for f in branches:
            if 'filter' in f:
                filter_objects.append(self.__simple_filter(identifier, f.get('filter')))
            elif 'left' in f:
                left = f.get('left')
                right = f.get('right')
                op = f.get('op')
                filter_objects.append(self.__complex_filter(identifier, left, right, op))
            else:
                raise NotImplementedError('nested filters: {}'.format(f))

        complex_filter = ComplexFilter(filter_objects[0], filter_objects[1], operator)
        complex_filter.identifier = identifier
        return complex_filter

    def __simple_filter(self, identifier, filter_conf):

        field = filter_conf.get('field')
        operator = filter_conf.get('op')
        value = filter_conf.get('value')

        if 'value' in filter_conf:
            self._value = filter_conf.get('value')
        elif 'enumerated' in filter_conf:
            # TODO: are enumerated values required/possible?
            # e.g. instead of type=1 -> type='CONNECT'
            raise NotImplementedError('Filtering with enumerated values: {}'.format(filter_conf.get('enumerated')))

        if (field and operator and value and identifier) is None:
            raise IncompleteFilterException('Filter: {}'.format(identifier))

        filter = SimpleFilter()
        filter.identifier = identifier
        filter.value = value
        filter.operator = operator
        filter.field = field

        return filter
