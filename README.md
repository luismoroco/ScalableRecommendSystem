# ScalableRecommendSystem
A distributed, scalable and fail tollerance Recommend System using large data.

# RUN 

1. Clone repository 
```bash
  git clone https://github.com/luismoroco/ScalableRecommendSystem.git
```
2. Init data and virtual enviorement VENV: (s) SMALL data 1MB || (f) FULL data 256MB
For example in SMALL data:
```bash
  bash ./setup.sh f 
```

3. Activate your VENV in your directory
```bash
  source venv/bin/activate
```

4. Setup the Cluster - DEV mode: (1)web + (2)Spark[master, node] + (1)db cassandra with REPLICATION=1
```bash
  sudo make setup
```

5. Start the preprocess. This contain a- clean data b-store data in db
```bash
  sudo make preprocess
```

6. For stop the container
```bash
  sudo make down
```

