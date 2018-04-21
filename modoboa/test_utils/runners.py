# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.test.simple import DjangoTestSuiteRunner
from django.utils.encoding import force_text
import operator
import time
from django.utils.unittest import TestSuite


TIMINGS = {}


def time_it(func):
    def _inner(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()

        TIMINGS[force_text(func)] = end - start
    return _inner


class TimingSuite(TestSuite):
    def addTest(self, test):  # NOQA:N802
        test = time_it(test)
        super(TimingSuite, self).addTest(test)


class TimedTestRunner(DjangoTestSuiteRunner):
    def build_suite(self, test_labels, extra_tests=None, **kwargs):
        suite = super(TimedTestRunner, self).build_suite(
            test_labels, extra_tests, **kwargs
        )
        return TimingSuite(suite)

    def teardown_test_environment(self, **kwargs):
        super(TimedTestRunner, self).teardown_test_environment(**kwargs)
        by_time = sorted(
            TIMINGS.items(),
            key=operator.itemgetter(1),
            reverse=True
        )[:10]
        print("Ten slowest tests:")
        for func_name, timing in by_time:
            print("{t:.2f}s {f}".format(f=func_name, t=timing))
