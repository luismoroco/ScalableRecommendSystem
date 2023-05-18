from dotenv import load_dotenv
import os 

load_dotenv('.env')

os.environ['PORT_CASSANDRA'] = os.getenv('C_NODE1_EXP_PORT')
os.environ['PASS_CASSANDRA'] = os.getenv('C_CLUSTER_PASS')
os.environ['USER_CASSANDRA'] = os.getenv('C_USERNAME')
