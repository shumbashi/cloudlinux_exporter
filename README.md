# Cloudlinux Prometheus Exporter

A [Prometheus](https://prometheus.io/) exporter which scrapes metrics from [Cloudlinux LVE-Stats 2](https://docs.cloudlinux.com/cloudlinux_os_components/#lve-stats-2)

## Prerequisites

- cloudlinux-statistics: cloudlinux-statistics is a CLI utility that provides historical information about resource usage. Installed by default with lve-stats-2.2-2

## Getting started

### Build and run from source

**Prerequisites**:
- Python >= 2.7
- Git
- Pyinstaller 3.6

**Steps**:
```bash
sudo pip install pyinstaller==3.6
git clone https://github.com/shumbashi/cloudlinux_exporter.git
cd cloudlinux_exporter
pyinstaller --runtime-tmpdir /run/user/0 --onefile cloudlinux_exporter.py
```

This will generate a binary in the sub folder `dist`, alternatively you can download a pre-built binary from [here](https://github.com/shumbashi/cloudlinux_exporter/releases/)

### Installation

**Note**: Those instructions are tested on Cloudlinux/CentOS 7

Move the generated binary to a suitable location

```
mv dist/cloudlinux_exporter /usr/local/bin/cloudlinux_exporter
```

Create a systemd service file
```
vim /etc/systemd/system/cloudlinux_exporter.service
```

Copy and paste the following in the service definition file
```
[Unit]
Description=Prometheus Cloudlinux Exporter
Documentation=https://github.com/shumbashi/cloudlinux_exporter
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
ExecStart=/usr/local/bin/cloudlinux_exporter \
    --port 9103

[Install]
WantedBy=multi-user.target
```

**Note**: Change the port number to match your requirements

Reload systemd to recognize the new service file
```
sudo systemctl daemon-reload
```

Start the service
```
sudo systemctl start cloudlinux_exporter
```

Enable service auto-start on boot
```
sudo systemctl enable cloudlinux_exporter
```

You can test if the exporter is running correctly using `curl`
```
curl http://127.0.0.1:9103
```

**Note**: You need to configure your firewall to allow access to port `9103` only from your Prometheus server IP

### Prometheus Configuration

You can configure Prometheus scrapper by adding the following to prometheus.yml on your Prometheus server

```
  # cPanel Cloudlinux Exporter
  - job_name: 'cloudlinux'
    relabel_configs:
    - source_labels: [__address__]
      regex: "([^:]+):\\d+"
      target_label: instance
    static_configs:
    - targets: ['SERVER_ADDRESS:9103']
```
Replace SERVER_ADDRESS with your Cloudlinux server IP or Hostname

## Sample Metrics
```
# HELP cloudlinux_collector_collect_seconds Time spent to collect metrics from Cloulinux
# TYPE cloudlinux_collector_collect_seconds summary
cloudlinux_collector_collect_seconds_count 3305.0
cloudlinux_collector_collect_seconds_sum 4126.327961444855
# HELP cloudlinux_collector_collect_seconds_created Time spent to collect metrics from Cloulinux
# TYPE cloudlinux_collector_collect_seconds_created gauge
cloudlinux_collector_collect_seconds_created 1.601718443124312e+09
# HELP cloudlinux_usage_pmem_lve Cloudlinux Usage PMEM LVE
# TYPE cloudlinux_usage_pmem_lve gauge
cloudlinux_usage_pmem_lve{domain="domain.ly",instance="cloudlinux231.server.ly",user="demouser"} 1.8944e+06
# HELP cloudlinux_usage_ep_lve Cloudlinux Usage EP LVE
# TYPE cloudlinux_usage_ep_lve gauge
cloudlinux_usage_ep_lve{domain="domain.ly",instance="cloudlinux231.server.ly",user="demouser"} 0.0
# HELP cloudlinux_usage_io_lve Cloudlinux Usage IO LVE
# TYPE cloudlinux_usage_io_lve gauge
cloudlinux_usage_io_lve{domain="domain.ly",instance="cloudlinux231.server.ly",user="demouser"} 0.0
# HELP cloudlinux_usage_io_mysql Cloudlinux Usage IO MySQL
# TYPE cloudlinux_usage_io_mysql gauge
cloudlinux_usage_io_mysql{domain="domain.ly",instance="cloudlinux231.server.ly",user="demouser"} 0.0
# HELP cloudlinux_usage_cpu_mysql Cloudlinux Usage CPU MySQL
# TYPE cloudlinux_usage_cpu_mysql gauge
cloudlinux_usage_cpu_mysql{domain="domain.ly",instance="cloudlinux231.server.ly",user="demouser"} 0.0
# HELP cloudlinux_usage_nproc_lve Cloudlinux Usage NPROC LVE
# TYPE cloudlinux_usage_nproc_lve gauge
cloudlinux_usage_nproc_lve{domain="domain.ly",instance="cloudlinux231.server.ly",user="demouser"} 0.0
# HELP cloudlinux_usage_vmem_lve Cloudlinux Usage VMEM LVE
# TYPE cloudlinux_usage_vmem_lve gauge
cloudlinux_usage_vmem_lve{domain="domain.ly",instance="cloudlinux231.server.ly",user="demouser"} 188416.0
# HELP cloudlinux_usage_iops_lve Cloudlinux Usage IOPS LVE
# TYPE cloudlinux_usage_iops_lve gauge
cloudlinux_usage_iops_lve{domain="domain.ly",instance="cloudlinux231.server.ly",user="demouser"} 0.0
# HELP cloudlinux_usage_cpu_lve Cloudlinux Usage CPU LVE
# TYPE cloudlinux_usage_cpu_lve gauge
cloudlinux_usage_cpu_lve{domain="domain.ly",instance="cloudlinux231.server.ly",user="demouser"} 4.672
# HELP cloudlinux_limits_pmem_lve Cloudlinux Limits PMEM LVE
# TYPE cloudlinux_limits_pmem_lve gauge
cloudlinux_limits_pmem_lve{domain="domain.ly",instance="cloudlinux231.server.ly",user="demouser"} 1.073741824e+09
# HELP cloudlinux_limits_ep_lve Cloudlinux Limits EP LVE
# TYPE cloudlinux_limits_ep_lve gauge
cloudlinux_limits_ep_lve{domain="domain.ly",instance="cloudlinux231.server.ly",user="demouser"} 20.0
# HELP cloudlinux_limits_io_lve Cloudlinux Limits IO LVE
# TYPE cloudlinux_limits_io_lve gauge
cloudlinux_limits_io_lve{domain="domain.ly",instance="cloudlinux231.server.ly",user="demouser"} 1.048576e+06
# HELP cloudlinux_limits_io_mysql Cloudlinux Limits IO MySQL
# TYPE cloudlinux_limits_io_mysql gauge
cloudlinux_limits_io_mysql{domain="domain.ly",instance="cloudlinux231.server.ly",user="demouser"} 1.999998976e+09
# HELP cloudlinux_limits_cpu_mysql Cloudlinux Limits CPU MySQL
# TYPE cloudlinux_limits_cpu_mysql gauge
cloudlinux_limits_cpu_mysql{domain="domain.ly",instance="cloudlinux231.server.ly",user="demouser"} 400.0
# HELP cloudlinux_limits_nproc_lve Cloudlinux Limits NPROC LVE
# TYPE cloudlinux_limits_nproc_lve gauge
cloudlinux_limits_nproc_lve{domain="domain.ly",instance="cloudlinux231.server.ly",user="demouser"} 100.0
# HELP cloudlinux_limits_vmem_lve Cloudlinux Limits VMEM LVE
# TYPE cloudlinux_limits_vmem_lve gauge
cloudlinux_limits_vmem_lve{domain="domain.ly",instance="cloudlinux231.server.ly",user="demouser"} 0.0
# HELP cloudlinux_limits_iops_lve Cloudlinux Limits IOPS LVE
# TYPE cloudlinux_limits_iops_lve gauge
cloudlinux_limits_iops_lve{domain="domain.ly",instance="cloudlinux231.server.ly",user="demouser"} 1024.0
# HELP cloudlinux_limits_cpu_lve Cloudlinux Limits CPU LVE
# TYPE cloudlinux_limits_cpu_lve gauge
cloudlinux_limits_cpu_lve{domain="domain.ly",instance="cloudlinux231.server.ly",user="demouser"} 100.0
# HELP cloudlinux_faults_pmem_lve Cloudlinux Faults PMEM LVE
# TYPE cloudlinux_faults_pmem_lve gauge
cloudlinux_faults_pmem_lve{domain="domain.ly",instance="cloudlinux231.server.ly",user="demouser"} 0.0
# HELP cloudlinux_faults_ep_lve Cloudlinux Faults EP LVE
# TYPE cloudlinux_faults_ep_lve gauge
cloudlinux_faults_ep_lve{domain="domain.ly",instance="cloudlinux231.server.ly",user="demouser"} 0.0
# HELP cloudlinux_faults_io_lve Cloudlinux Faults IO LVE
# TYPE cloudlinux_faults_io_lve gauge
cloudlinux_faults_io_lve{domain="domain.ly",instance="cloudlinux231.server.ly",user="demouser"} 0.0
# HELP cloudlinux_faults_io_mysql Cloudlinux Faults IO MySQL
# TYPE cloudlinux_faults_io_mysql gauge
cloudlinux_faults_io_mysql{domain="domain.ly",instance="cloudlinux231.server.ly",user="demouser"} 0.0
# HELP cloudlinux_faults_cpu_mysql Cloudlinux Faults CPU MySQL
# TYPE cloudlinux_faults_cpu_mysql gauge
cloudlinux_faults_cpu_mysql{domain="domain.ly",instance="cloudlinux231.server.ly",user="demouser"} 0.0
# HELP cloudlinux_faults_nproc_lve Cloudlinux Faults NPROC LVE
# TYPE cloudlinux_faults_nproc_lve gauge
cloudlinux_faults_nproc_lve{domain="domain.ly",instance="cloudlinux231.server.ly",user="demouser"} 0.0
# HELP cloudlinux_faults_vmem_lve Cloudlinux Faults VMEM LVE
# TYPE cloudlinux_faults_vmem_lve gauge
cloudlinux_faults_vmem_lve{domain="domain.ly",instance="cloudlinux231.server.ly",user="demouser"} 0.0
# HELP cloudlinux_faults_iops_lve Cloudlinux Faults IOPS LVE
# TYPE cloudlinux_faults_iops_lve gauge
cloudlinux_faults_iops_lve{domain="domain.ly",instance="cloudlinux231.server.ly",user="demouser"} 0.0
# HELP cloudlinux_faults_cpu_lve Cloudlinux Faults CPU LVE
# TYPE cloudlinux_faults_cpu_lve gauge
cloudlinux_faults_cpu_lve{domain="domain.ly",instance="cloudlinux231.server.ly",user="demouser"} 0.0
```

## Sample Dashboard
Here is a sample dashboard created using [Grafana](https://github.com/grafana/grafana) with metrics from `cloudlinux_exporter`
