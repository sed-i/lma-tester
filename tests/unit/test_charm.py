# Copyright 2021 Canonical Ltd.
# See LICENSE file for licensing details.


import unittest

from ops.testing import Harness

from charm import LmaTesterCharm


class TestCharm(unittest.TestCase):
    def test_charm(self):
        harness = Harness(LmaTesterCharm)
        self.addCleanup(harness.cleanup)
        harness.begin()
        pass
