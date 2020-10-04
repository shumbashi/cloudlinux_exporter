import json
from sys import exit
import time
import argparse
import os
import subprocess
import platform

from prometheus_client import start_http_server, Summary
from prometheus_client.core import GaugeMetricFamily, REGISTRY

COLLECTION_TIME = Summary('cloudlinux_collector_collect_seconds', 'Time spent to collect metrics from Cloulinux')

class CloudlinuxCollector(object):
    hostname = platform.node()
    metric_classes = ["Usage", "Limits", "Faults"]
    metric_types = ["CPU", "EP", "VMEM", "PMEM", "NPROC", "IO", "IOPS"]

    def collect(self):
        start = time.time()
        self._setup_empty_prometheus_metrics()

        results = self._get_metrics()
        json_results = json.loads(results)
        for user in json_results['users']:
            self._parse_metrics(user)

        for metric_class in self.metric_classes:
            for metric in self._prometheus_metrics[metric_class.lower()].values():
                yield metric[0]
            
        duration = time.time() - start
        COLLECTION_TIME.observe(duration)

    def _setup_empty_prometheus_metrics(self):
        self._prometheus_metrics = {}
        for metric_class in self.metric_classes:
            self._prometheus_metrics[metric_class.lower()] = {}
            for metric_type in self.metric_types:
                self._prometheus_metrics[metric_class.lower()][metric_type.lower()+'_lve'] = GaugeMetricFamily('cloudlinux_{0}_{1}_lve'.format(metric_class.lower(), metric_type.lower()),
                                      'Cloudlinux {0} {1} LVE'.format(metric_class, metric_type), labels=["instance", "domain", "user"]),
                if metric_type == "CPU" or metric_type == "IO":
                    self._prometheus_metrics[metric_class.lower()][metric_type.lower()+'_mysql'] = GaugeMetricFamily('cloudlinux_{0}_{1}_mysql'.format(metric_class.lower(), metric_type.lower()),
                                      'Cloudlinux {0} {1} MySQL'.format(metric_class, metric_type), labels=["instance", "domain", "user"]),

    def _get_metrics(self):
        command = "/usr/sbin/cloudlinux-statistics --json"
        result,error  = subprocess.Popen(command, universal_newlines=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if error:
            print(error)
            exit(1)
        return result

    def _parse_metrics(self, user):
        name = user['domain']
        for metric_class in self.metric_classes:
            for metric_type in self.metric_types:
                self._prometheus_metrics[metric_class.lower()][metric_type.lower()+'_lve'][0].add_metric([self.hostname, user['domain'], user['username']], user[metric_class.lower()][metric_type.lower()]['lve'])
                if metric_type == "CPU" or metric_type == "IO":
                    if metric_class.lower() == 'faults':
                        self._prometheus_metrics[metric_class.lower()][metric_type.lower()+'_mysql'][0].add_metric([self.hostname, user['domain'], user['username']], 0)
                    else:
                        self._prometheus_metrics[metric_class.lower()][metric_type.lower()+'_mysql'][0].add_metric([self.hostname, user['domain'], user['username']], user[metric_class.lower()][metric_type.lower()]['mysql'])

def parse_args():
    parser = argparse.ArgumentParser(
        description='Cloudlinux exporter args metrics port'
    )
    parser.add_argument(
        '-p', '--port',
        metavar='port',
        required=False,
        type=int,
        help='Listen to this port',
        default=int(os.environ.get('VIRTUAL_PORT', '9118'))
    )
    return parser.parse_args()


def main():
    try:
        args = parse_args()
        port = int(args.port)
        REGISTRY.register(CloudlinuxCollector())
        start_http_server(port)
        print("Starting Cloudlinux Collector. Serving at port: {}".format(port))
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(" Interrupted")
        exit(0)

if __name__ == "__main__":
    main()    