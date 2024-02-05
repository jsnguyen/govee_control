import tomllib
import requests
import json
import time
import PySimpleGUI as sg

api_filename = '/Users/jsn/landing/projects/govee_control/api_key.toml'

with open(api_filename, 'rb') as f:
    key = tomllib.load(f)['key']

headers = {'Govee-API-Key': key,
           'Content-Type': 'application/json'}
base_url = 'https://developer-api.govee.com/v1/'

def get_devices_list():
    devices_url = base_url+'devices/'

    response = requests.get(devices_url, headers=headers)
    return response

# value can be 'on' or 'off'
def turn_on_off(devices, value):

    control_url = base_url+'devices/control/'
    cmd = {'name': 'turn', 'value': value}

    responses = []
    for d in devices:
        device = d['device']
        deviceName = d['deviceName']
        model = d['model']

        body= {'device': device, 'model': model, 'cmd': cmd}

        responses.append(requests.put(control_url, json=body, headers=headers))
    return responses

# can be 'min' or 'max'
def set_color_tem(devices, minmax):

    control_url = base_url+'devices/control/'

    responses = []
    for d in devices:
        device = d['device']
        deviceName = d['deviceName']
        model = d['model']

        tem = d['properties']['colorTem']['range'][minmax]

        cmd = {'name': 'colorTem', 'value': tem}

        body= {'device': device, 'model': model, 'cmd': cmd}

        responses.append(requests.put(control_url, json=body, headers=headers))
    return responses

# 1 to 100
def set_brightness(devices, value):
    control_url = base_url+'devices/control/'

    responses = []
    for d in devices:
        device = d['device']
        deviceName = d['deviceName']
        model = d['model']

        cmd = {'name': 'brightness', 'value': value}

        body= {'device': device, 'model': model, 'cmd': cmd}

        responses.append(requests.put(control_url, json=body, headers=headers))
    return responses

def gui():

    res = get_devices_list()
    devices = res.json()['data']['devices']
    device_names = [d['deviceName'] for d in devices]
    
    names = ['Floor Lamp', 'Desk Lamp', 'Wall Lamp']
    t_devi = []
    for i,n in enumerate(names):
        if n in device_names:
            color='green'
        else:
            color='red'
        
        t_devi.append([sg.Text(n, size=(16,1), text_color='white', background_color=color, justification='center', key='N{}'.format(i))])

    f_devi = sg.Frame('Status', t_devi)

    b_temp = [sg.Button('Cool', size=(5,2)), sg.Button('Warm', size=(5,2))]
    f_temp = sg.Frame('Temperature', [b_temp])

    b_brig = [sg.Button('Bright', size=(5,2)), sg.Button('Dim', size=(5,2))]
    f_brig = sg.Frame('Brightness', [b_brig])

    b_stat = [sg.Button('On', size=(5,2)), sg.Button('Off', size=(5,2))]
    f_stat = sg.Frame('State', [b_stat])

    output = [sg.Text('', size=(28,6), text_color='black', background_color='white', key='OUTPUT')]
    f_outp = sg.Frame("Output", [output], title_color='blue')

    layout = [[f_devi], [f_temp], [f_brig], [f_stat], [f_outp]]
    window = sg.Window('Govee Control', layout, size=(250, 450), element_justification='c')

    if res.status_code != 200:
        window['OUTPUT'].update(value = '{}: {}'.format(res.status_code, res.text))

    counter = 0
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Cool':
            ress = set_color_tem(devices, 'max')
        elif event == 'Warm':
            ress = set_color_tem(devices, 'min')
        elif event == 'Bright':
            ress = set_brightness(devices, 100)
        elif event == 'Dim':
            ress = set_brightness(devices, 25)
        elif event == 'On':
            ress = turn_on_off(devices, 'on')
        elif event == 'Off':
            ress = turn_on_off(devices, 'off')

        output = ''
        for res in ress:
            counter+=1
            if res.status_code == 200:
                output += '[{}]: {}\n'.format(counter, res.json()['message']) 
            else:
                output += '[{}] {}: {}\n'.format(counter, res.status_code, res.text) 
        window['OUTPUT'].update(value = output)

    window.close()

gui()
