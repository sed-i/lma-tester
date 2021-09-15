import random
import time

from prometheus_client import start_http_server, Gauge, Summary


# Metric that tracks time spent and number of requests made.
REQUEST_TIME = Summary('request_processing_seconds',
                       'Time spent processing request')

dummy_gauges = [Gauge(f"gauge_{i}", f"Dummy gauge {i}") for i in range(20)]


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

        for gauge in dummy_gauges:
            gauge.set(random.randint(1, 100))


if __name__ == '__main__':
    main()
