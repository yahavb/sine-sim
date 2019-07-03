from chalice import Chalice
import json
import numpy as np
from time import gmtime,strftime
from urlparse import urlparse, parse_qs
import boto3


app = Chalice(app_name='sine-simu')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('observations')


def deserializer(items,observations):
    print('in deserializer '+str(items))
    items=items.replace("[","") 
    items=items.replace("]","") 
    print('items='+str(items))
    for num in items.split(" "):
       if (num):
         print('num='+str(num))
         observations.append(float(num))

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

@app.route('/latest_gs_inference')
def get_latest_gs_inference():
    print('in get_inferences')
    observations=[]
    response = table.get_item(
    Key={
      'key': 'observation'
    }
    )
    x=json.dumps(response['Item'])
    print(x)
    item = response['Item']['value']
    print(item)
    deserializer(item,observations)
    print('observations='+str(observations))
    #inference=np.percentile(observations,90)
    return {"Prediction":{"observations": observations}}
    #return {"Prediction":{"num_of_gameservers": str(inference)}}

def get_last_obs_arr():
    print('in get_last_obs_arr')
    observations=[]
    response = table.get_item(
    Key={
      'key': 'observation'
    }
    )
    x=json.dumps(response['Item'])
    item = response['Item']['value']
    deserializer(item,observations)
    print('observations='+str(observations))
    return observations

@app.route('/put_latest_gs_inference/{value}')
def put_latest_gs_inference(value):
    print ('in put_latest_gs_inference='+str(value))
    observations=get_last_obs_arr()
    observations=observations[1:]
    observations=np.append(observations,float(value))
    observations=str(observations)
    print ('observations='+observations)
    table.put_item(
       Item={
          'key': 'observation',
          'value': observations
       }
    )
    return {"Inference":{"value": str(observations)}}
