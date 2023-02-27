# breast-cancer-pipeline
A Breast Cancer pipeline distributed locally.

[Docs](https://carlos-eduardo-sanchez-torres.sanchezcarlosjr.com/MexicanPACS-a-Breast-Cancer-risk-estimation-at-a-public-Mexican-hospital-7a807c1db3b641378180b0c60633c38b)

# Installation
Install on each node in your cluster this repository using the below command.

Using curl
```bash
bash <(curl -s https://raw.githubusercontent.com/sanchezcarlosjr/breast-cancer-pipeline/main/installer)
```

# Getting started
Activate the environment on each node
```bash
source env/bin/activate
```

Start the head node
```bash
ray start --head --port=6379
```

Connect the nodes to head node
```bash
ray start --address='ADDRESS:PORT'
```

On the head node, start the pipeline
```bash
python pipeline.py
```
