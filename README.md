# DevOps: Flask task

### I. Creating Image for app.py

Firstly, we create a folder named `/app`, which will contain everything mandatory for the application itself. Besides uploading the code, we also need a corresponding  `Dockerfile` - template, stating the instructions for the consequent container creation. There are some lines we'd like to dive into:

```
RUN pip3.8 install flask
```

We only need a single flask package for the app to be running, since it interrogates with this framework. By the way, pip's version is dictated by the inherited image's version of Python. 

After, several standard lines can be found, mainly focused on establishing a particular working directory and copying there everything vital. Last thing to be mentioned here is the command, being a key part of the entire document. 

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

This is a fairly classic set up, presented in the most of such tasks (including documentation). Nevertheless, there is another key file for easily running the entire system. It is called `graph_config.json`, being placed into `/dashboard` directory. Probably, no broad definitions is needed here since most of the configuration is copied from the convinient Graphana interace already in json format. The only thing to be explicitly described is the metric's statement. Rate per second can be accessed via the following command 

```
rate(hello_world_counter{status=}[interval]
```

### IV. Declaring dockers' Composition

Here we reach our major configuration file. It is a docker compose - powerful tool for encapsulting and interconnecting several containers. Our comprehensive architecture will start from **(1)** app container, followed by **(2)** Prometheus module, passing all data from metric to **(3)** Grafana. Besides, the `docker-compose.dev.yml` programm itself will provide the specific instructions on project's organization. Hence, we declare 3 separate services (=containers). First will be directly devoted to our application:

```
app:
    container_name: app
    build:
      context: app
    ports:
    - 8000:5000
```

We set a reasonable label for the service, as well as provide a non-mandatory container name for resilence. We also specify the context path to the directory with corresponding `Dockerfile` for the `build` parameter. The ports reveal relationship host-container. When we analyze productivity of our server, we will connect the http://localhost:8000/.

If speaking of the Prometheus part, here is a well-known embodiement:

```
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    volumes:
      - ./prometheus/config.yml:/etc/prometheus/prometheus.yml
    ports:
      - 9090:9090
    depends_on:
      - app
```

Obviously, we use the already existing image of latest module's version. Volumes stand for an extensions for the service (configuration in this case). While a long-form syntax is available, we prefer classical Source:Target statement. Last parameter puts the container in a specific place of `docker-compose` dependancy order, used when running the architecture. Mostly the same can be said about Grafana section, except we use more volumes (dashboards & datasources configurations, as well as particular graph description in json format), select different ports and put it at the last place when activating.

### V. Command Line

Everything is really simple. While the following two commands can be joined into single one, we rather make our process multistage and transparent. As a start, we build our docker composition after entering the working directory through terminal:

```
$ docker compose -f docker-compose.dev.yml build --no-cache
```

Cache elimination is added in case of wrong implementations and corrections during programm's establishment.

```
$ docker compose -f docker-compose.dev.yml up 
```

This simply activates in the given order all the containers. By accessing the 8000 port, we can get an announced line and counter of total visits after launch. Meanwhile, terminal sends messages about success of each installation/operations and constabtly sends messages of the application's work if everything is fine.

Now let's load our server with a help of Apache Bench - great benchmarking tool for measuring servers' perfomance. 

```
$  ab -n 30000 -c 100 http://localhost:8000/ 
```

Apache Bench will send to port 8000 exactly 30000 requests with approximately 100 concurrent ones. Section **VI** contains a graph from Grafana dashboard, depicting exactly this period. What really intresting is the reports `apache_logs.txt`. Besides all the provided information, we can explore the 100% level of completed requests with a mean processing of 0.8 seconds with 1.7 being the worst result. 'Requests per second' line in our inference with a mean of 114 requests per second shows successful completion of this little challenge by our server.


### Dashboard visualization

![](graph.png)
