from chalice import Chalice
import json
import numpy as np
from time import gmtime,strftime
from urlparse import urlparse, parse_qs
import boto3


app = Chalice(app_name='sine-simu')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('observations')

class Observation:
   history = []
   def __init__(self):
        print("in __init__")
        self.demand_history_len=5
   
   def append_obs(self,obs):
        print('in append_obs')
        self.history=self.history[1:] # shift the observation by one to remove one history point
        self.history=np.append(self.history,obs)
        print(self.history)

   def get_history(self):
        return self.history

observations=Observation()

@app.route('/')
def index():
    return {'sine': 'num'}

@app.route('/sine/{value}')
def get_sine(value):
    num=float(value)
    print(num)
    sine=44*np.sin(num)
    print(sine)
    return {"Prediction":{"num_of_gameservers": sine}}


@app.route('/currsine1h')
def get_curr_sine1h():
    cycle_arr=sinearr=np.linspace(0.2,3.1,61)
    current_min=strftime("%M", gmtime())
    print("current_min="+str(current_min))

    current_point=cycle_arr[int(current_min)]
    print("current_point="+str(current_point))
    sine=44*np.sin(current_point)
    print("sine="+str(sine))
    return {"Prediction":{"num_of_gameservers": sine}}

@app.route('/currsine2h')
def get_curr_sine2h():
    cycle_arr=sinearr=np.linspace(0.2,3.1,121)
    current_min=strftime("%M", gmtime())
    print("current_min="+str(current_min))
    current_hour=int(strftime("%I", gmtime()))
    print("current_hour="+str(current_hour))

    if (current_hour%2):
       current_point=cycle_arr[int(current_min)]
    else:
       current_point=cycle_arr[int(current_min)+60]
    print("current_point="+str(current_point))
    sine=44*np.sin(current_point)
    print("sine="+str(sine))
    return {"Prediction":{"num_of_gameservers": sine}}

@app.route('/inferences')
def get_inferences():
    print('in get_inferences')
    response = table.get_item(
    Key={
      'key': 'observation'
    }
    )
    x=json.dumps(response['Item'])
    print(x)
    item = response['Item']['value']
    observation=json.dumps(item)
    return {"Prediction":{"num_of_gameservers": observation}}
