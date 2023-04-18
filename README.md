# DevOps: Flask task

### I. Creating Image for app.py

Firstly, we create a folder named <ins>app</ins> which will contain everything, mandatory for the application itself. Besides uploading the code, we also need a corresponding  <ins>Dockerfile</ins> - template, stating the instructions for the consequent container creation. There are some lines we'd like to dive into:

```
RUN pip3.8 install flask
```

We only need a single flask package for the app to be running, since it interrogates with this framework. By the way, pip's version is dictated by the inherited image's version of Python. 

After that several standard lines can be found, mainly focused on establishing a particular working directory and copying there everything vital. Last thing to be mentioned here is the command, being a key part of the entire document. 


```
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
```

It orders to run a python3 flask framework with a specific zero host for external visibility control.

### Dashboard visualization

![](graph.png)
