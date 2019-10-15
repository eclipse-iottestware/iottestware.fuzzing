import unittest

from tests.fuzzer.test_generator import TestGenerator
from tests.fuzzer.test_rulesengine import TestRulesEngine
# from tests.fuzzer.test_filter import TestFilter
from tests.fuzzer.test_operators import TestOperators


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestRulesEngine('test_rules_engine'))
    # suite.addTest(TestFilter('test_matching_filters'))    # TODO: fix tests
    suite.addTest(TestGenerator('test_fuzz_generator'))
    suite.addTest(TestOperators('test_operators'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
