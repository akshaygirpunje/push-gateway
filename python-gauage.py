import prometheus_client as prom
import requests
import time
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway


RESPONSE_TIME_GAUGE = prom.Gauge('sample_external_url_response_ms', 'Url response time in ms', ["url"])
URL_LIST = ["https://httpstat.us/200", "https://httpstat.us/503"]


def get_response(url):
    response = requests.get(url)
    response_time = response.elapsed.total_seconds()
    print(url,'--->',response_time)    
    return response_time


def get_url_status():
    while True:
        for url_name in URL_LIST:
            response_time = get_response(url_name)
            RESPONSE_TIME_GAUGE.labels(url=url_name).set(response_time)
            response = requests.get(url_name)
            url_status_code=response.status_code
            print(url_name,'--->',url_status_code)
            if(url_status_code == 200):
              value1=1
              registry = CollectorRegistry()
              g = Gauge('sample_external_url_up', 'Boolean status of site up or down', registry=registry)
              g.set(value1)   # Set to a given value
              push_to_gateway('52.35.140.185:30963', 'url=https://httpstat.us/200',registry=registry)
              g = Gauge('sample_external_url_response_ms', 'HTTP response in milliseconds', registry=registry)
              g.set(response_time)   # Set to a given value
              push_to_gateway('52.35.140.185:30963', 'url=https://httpstat.us/200',registry=registry)

            if(url_status_code == 503):
              value1=0
              registry = CollectorRegistry()
              g = Gauge('sample_external_url_up', 'Boolean status of site up or down', registry=registry)
              g.set(value1)   # Set to a given value
              push_to_gateway('52.35.140.185:30963', 'url=https://httpstat.us/503',registry=registry)
              g = Gauge('sample_external_url_response_ms', 'HTTP response in milliseconds', registry=registry)
              g.set(response_time)   # Set to a given value
              push_to_gateway('52.35.140.185:30963', 'url=https://httpstat.us/503',registry=registry)

            time.sleep(5)


if __name__ == '__main__':
    prom.start_http_server(8001)
    get_url_status()
