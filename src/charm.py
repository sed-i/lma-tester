#!/usr/bin/env python3
# Copyright 2021 Canonical Ltd.
# See LICENSE file for licensing details.

"""A Charm to functionally test the Prometheus Operator"""

import logging

from ops.charm import CharmBase
from ops.main import main
from ops.framework import StoredState
from ops.model import ActiveStatus

logger = logging.getLogger(__name__)


class PrometheusTesterCharm(CharmBase):
    """Charm the service."""

    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.on.show_config_action, self._on_show_config_action)

    def _on_install(self, _):
        self.unit.status = ActiveStatus()

    def _on_config_changed(self, _):
        pass

    def _on_show_config_action(self, event):
        event.set_results({"config": self.model.config})


if __name__ == "__main__":
    main(PrometheusTesterCharm)
