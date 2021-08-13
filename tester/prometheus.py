import os
import random
import time

from prometheus_client import start_http_server, Gauge, Summary


# Metric that tracks time spent and number of requests made.
REQUEST_TIME = Summary('request_processing_seconds',
                       'Time spent processing request')

ALERT_CONDITION_1 = Gauge('gauge_1',
                          'Completely meaningless value to trigger alerts')

ALERT_CONDITION_2 = Gauge('gauge_2',
                          'Completely meaningless value to trigger alerts')


@REQUEST_TIME.time()
def process_request(t):
    """A fake function that takes a configurable amount of time.

    Args:
        t: integer specifying amount of time that should be
           spent in processing this request
    """
    time.sleep(t)


def main(port=8000):
    """Expose a metrics endpoint to prometheus"""
    start_http_server(port)

    while True:
        process_request(random.random())

        if os.getenv("TESTER_TRIGGER_GAUGE_1", ""):
            ALERT_CONDITION_1.set(random.randint(11, 100))
        else:
            ALERT_CONDITION_1.set(random.randint(1, 9))

        if os.getenv("TESTER_TRIGGER_GAUGE_2", ""):
            ALERT_CONDITION_2.set(random.randint(11, 100))
        else:
            ALERT_CONDITION_2.set(random.randint(1, 9))


if __name__ == '__main__':
    main()
