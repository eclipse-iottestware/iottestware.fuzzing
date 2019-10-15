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

from abc import ABC, abstractmethod

import sympy as sy
import numpy as np


class AbstractUrn(ABC):

    def __init__(self, num_elements):
        self._num_elements = num_elements

        if num_elements <= 0:
            raise Exception('An Abstract Urn Model must have at least 1 element')

    @property
    def num_elements(self):
        return self._num_elements   # TODO: right term?

    @abstractmethod
    def choose_element(self):
        """
        according to the concrete urn model und configuration return an index
        :return: index of the taken element
        """
        pass


class Multinomial(AbstractUrn):

    def __init__(self, strengths, nxp=3, seed=None):
        super().__init__(len(strengths))
        self._strengths = strengths
        self._sum_strengths = sum(strengths)
        self._nxp = nxp
        self._rnd = np.random.RandomState(seed)

        self._weights = []
        for s in strengths:
            self._weights.append(sy.Rational('{}/{}'.format(s, self._sum_strengths)))

    def __str__(self):
        return 'MultinomialDistribution {}'.format(self._weights)

    @property
    def weights(self):
        return self._weights

    def choose_element(self):
        dist = self._rnd.multinomial(self._nxp, self._weights)
        chosen = np.argmax(dist)
        return chosen
