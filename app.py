from chalice import Chalice
import numpy as np
from time import gmtime,strftime


app = Chalice(app_name='sine-simu')

cycle_arr=sinearr=np.linspace(0.2,3.1,120)

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


@app.route('/currsine')
def get_curr_sine():
    current_min=strftime("%M", gmtime())
    print(current_min)
    if (current_min>59):
        current_point=cycle_arr[int(current_min)+60]
    else:
        current_point=cycle_arr[int(current_min)]
    sine=44*np.sin(current_point)
    print(sine)
    return {"Prediction":{"num_of_gameservers": sine}}

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
