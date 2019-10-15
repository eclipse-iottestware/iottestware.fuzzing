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


class BuilderException(Exception):
    pass


class IncompleteFilterException(Exception):
    pass


class AbstractBuilder(ABC):

    @abstractmethod
    def build_from_config(self, config):
        pass

    '''
    def build(self):
        """
        Possible future case: a builder is configured via public API instead from a config.
        Basically the main reason to have this abstract class here!
        :return:
        """
        raise NotImplementedError('stateful build of generator builder')
    '''
