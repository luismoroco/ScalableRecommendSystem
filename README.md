# ScalableRecommendSystem
A distributed, scalable and fail tollerance Recommend System using large data.

# RUN 

Clone repository 
```bash
  git clone https://github.com/luismoroco/ScalableRecommendSystem.git
```
Init data and virtual enviorement VENV: (s) SMALL data 1MB || (f) FULL data 256MB
For example in SMALL data:
```bash
  bash ./init.sh s 
```

Activate your VENV in your directory
```bash
  source venv/bin/activate
```

Setup the Cluster - DEV mode: (1)web + (2)Spark[master, node] + (1)db cassandra with REPLICATION=1
```bash
  sudo make setup
```