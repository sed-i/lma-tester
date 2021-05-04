# Copyright 2021 Canonical Ltd
# See LICENSE file for licensing details.


import unittest

from ops.testing import Harness
from charm import PrometheusTesterCharm


class TestCharm(unittest.TestCase):
    def test_charm(self):
        harness = Harness(PrometheusTesterCharm)
        self.addCleanup(harness.cleanup)
        harness.begin()
        pass
