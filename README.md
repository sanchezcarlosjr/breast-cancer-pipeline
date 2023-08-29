# breast-cancer-pipeline
A Breast Cancer pipeline distributed on promise.

[Docs](https://carlos-eduardo-sanchez-torres.sanchezcarlosjr.com/MexicanPACS-a-Breast-Cancer-risk-estimation-at-a-public-Mexican-hospital-7a807c1db3b641378180b0c60633c38b)

# Installation
Install on each node in your cluster this repository using the below command. Write your own settings.

Using curl
```bash
bash <(curl -s https://raw.githubusercontent.com/sanchezcarlosjr/breast-cancer-pipeline/main/installer) http://127.0.0.1:9000/cases/.env
```

# Getting started
## Environment
Choose some head and change its environment. 
```bash 
IS_HEAD=true
```

## Start the execution in each node
```
make exec
```

## Visualize an image from npy file.
```
make npy url="localhost:9000/[...].npy"
```


## Pipelines
### V1
The first pipeline is based on 

