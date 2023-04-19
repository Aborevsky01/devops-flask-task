# DevOps: Flask task

### I. Creating Image for app.py

Firstly, we create a folder named `/app` which will contain everything, mandatory for the application itself. Besides uploading the code, we also need a corresponding  `Dockerfile` - template, stating the instructions for the consequent container creation. There are some lines we'd like to dive into:

```
RUN pip3.8 install flask
```

We only need a single flask package for the app to be running, since it interrogates with this framework. By the way, pip's version is dictated by the inherited image's version of Python. 

After that several standard lines can be found, mainly focused on establishing a particular working directory and copying there everything vital. Last thing to be mentioned here is the command, being a key part of the entire document. 


```
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
```

It orders to run a python3 flask framework with a specific zero host for external visibility control.

### II. Configuration of Prometheus

Prometheus is a well-known monitoring system. This tool will allow us to collect and store target metric for further visualization, being an intermediate phase of the entire deployed architecture. So, we need a specific adjustment for the default configuration. 

```
global:
  scrape_interval: 1s
  rule_files:
```

First parameter is defining the metric's collection interval. The latter is pointless for our task and simply stands for list of files that need to be executed before, available for all the read ones.

After the global section we reach the next one: scrape configurations.

```
scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["prometheus:9090"]

  - job_name: "Server 5000"
    static_configs:
      - targets: ["app:5000"]
```

We assign a name for each job and provide a `static_configs` section, where statically set a particular target metric. By the way, the one more intresting for one comes from localhost 5000, being appointed for out application (the second job).

### III. Setting Grafana

We finally approach our software tool, designed for data analysis and visualization. Grafana provides us with a dashboard, built based on values, coming from prometheus container. 

Launch of grafana and its introduction into our service requires several configurations. First is responsible for coherent collection of data sources. 

```
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    editable: true
    is_default: true
    access: proxy
    url: http://prometheus:9090
```

We basically have a single metric. Its values are coming from Prometheus, having no permission to edit and located at the standard url. However, besides establishing a connection to the previous monitor in our sequence, we also need to set rules for the output dashboards (not to be confused with graphs configuration).

```
apiVersion: 1

providers:
  - name: "Prometheus"
    orgId: 1
    folder: ""
    type: file
    disableDeletion: false
    editable: true
    options:
      path: /var/lib/grafana/dashboards
```

This is a fairly classic set up, presented in the most of such tasks (including documentation). Nevertheless, there is another key file for easily running the entire system. It is called `graph_config.json`, being placed into `/dashboard` directory. Probably, no broad definitions is needed here since most of the configuration is copied from the convinient Graphana interace already in json format.

### IV. Declaring dockers' Composition

### V. Command Line

### Dashboard visualization

![](graph.png)
