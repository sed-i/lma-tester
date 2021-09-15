#!/usr/bin/env python3
# Copyright 2021 Canonical Ltd.
# See LICENSE file for licensing details.

"""A Charm to functionally test the Prometheus Operator."""

import logging

from charms.prometheus_k8s.v0.prometheus import MetricsEndpointProvider
from ops.charm import CharmBase
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus, WaitingStatus
from ops.pebble import ConnectionError

logger = logging.getLogger(__name__)


class LmaTesterCharm(CharmBase):
    """Charm the service."""

    _relation_name = "metrics-endpoint"
    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self._stored.set_default(monitoring_enabled=False)
        jobs = [{"static_configs": [{"targets": ["*:8000"], "labels": {"status": "testing"}}]}]
        self.metrics_endpoint = MetricsEndpointProvider(
            self, self._relation_name, self.on.lma_tester_pebble_ready, jobs=jobs
        )
        self.framework.observe(self.on.lma_tester_pebble_ready, self._ensure_application_runs)
        self.framework.observe(self.on.upgrade_charm, self._ensure_application_runs)
        self.framework.observe(self.on.update_status, self._ensure_application_runs)
        self.framework.observe(self.on.config_changed, self._ensure_application_runs)
        self.framework.observe(self.on.show_config_action, self._on_show_config_action)

    def _ensure_application_runs(self, event):
        rel = self.framework.model.get_relation(self._relation_name)
        if rel and not self._stored.monitoring_enabled:
            binding = self.model.get_binding(rel)
            bind_address = str(binding.network.bind_address)
            self._stored.monitoring_enabled = True
            logger.debug("NETWORK : %s", bind_address)

        container = self.unit.get_container("lma-tester")

        if container.can_connect():
            layer = self._tester_pebble_layer()
            container.add_layer("tester", layer, combine=True)

            try:
                service = container.get_service("tester")
            except ConnectionError:
                logger.debug("Pebble API is not yet ready")
                event.defer()
                return

            if service.is_running():
                container.stop("tester")
                logger.info("Restarted tester service")
            else:
                logger.info("Started tester service")

            container.start("tester")

            self.unit.status = ActiveStatus()
        else:
            logger.debug("Pebble in the lma-tester container is not ready")
            self.unit.status = WaitingStatus("Waiting for pebble")

    def _on_show_config_action(self, event):
        event.set_results({"config": self.model.config})

    def _tester_pebble_layer(self):
        layer = {
            "summary": "prometheus tester",
            "description": "a test data generator for Prometheus",
            "services": {
                "tester": {
                    "override": "replace",
                    "summary": "tester service",
                    "command": "python /tester/tester.py",
                    "startup": "enabled",
                    "environment": {
                        "TESTER_TRIGGER_GAUGE_1": self.config["trigger_gauge_1_alert"] or "",
                        "TESTER_TRIGGER_GAUGE_2": self.config["trigger_gauge_2_alert"] or "",
                        "PYTHONPATH": "/var/lib/juju/agents/unit-lma-tester-0/charm/venv",
                    },
                }
            },
        }
        return layer

    @property
    def _consumes(self):
        return {"prometheus": ">=2.0"}


if __name__ == "__main__":
    main(LmaTesterCharm)
