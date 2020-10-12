import requests
from requests.auth import HTTPBasicAuth
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import server_data as serv
import time


def get_apparat_data(app_name='', need_graph=False):

    apparats_info = requests.get(url=serv.URL, headers=serv.HEADERS,
                                 auth=HTTPBasicAuth('apikey', serv.AUTH)).json()

    attempts_count = 0
    while not apparats_info and attempts_count < 100:
        print('Not returning a 200 response, try again')
        time.sleep(5)
        apparats_info = requests.get(url=serv.URL, headers=serv.HEADERS,
                                     auth=HTTPBasicAuth('apikey', serv.AUTH)).json()
        attempts_count += 1

    correct_app = False
    if app_name != '':
        if need_graph:
            for data in apparats_info:
                if data['tag'] == app_name:
                    correct_app = True
                    with open(f'{app_name}.txt', 'a') as f:
                        f.writelines(str(data['value']) + '\n')
                    return float(data['value'])
            if not correct_app:
                print('wrong app name')
                return 0
        else:
            while True:
                for data in apparats_info:
                    if data['tag'] == app_name:
                        correct_app = True
                        print(data['value'])
                        with open(f'{app_name}.txt', 'a') as f:
                            f.writelines(str(data['value']) + '\n')
                if not correct_app:
                    print('wrong app name')
                    return 0
                time.sleep(1)
    else:
        for apparat in apparats_info:
            print(apparat['tag'])


def create_plot(app=''):
    if app == '':
        print('Select apparat name')
        return 0
    fig, ax = plt.subplots()
    plt.grid(True)
    xdata, ydata = [], []
    ln, = plt.plot([], [], 'ro')


    def init():
        ax.set_xlim(0, serv.TIME_LIMIT)
        ax.set_ylim(0, 100)
        return ln,


    def update(frame):
        xdata.append(frame)
        print(frame)
        ydata.append(get_apparat_data(app_name=app, need_graph=True))
        ln.set_data(xdata, ydata)
        return ln,


    ani = FuncAnimation(fig, update, interval=serv.TIME_INTERVAL, init_func=init, blit=True)
    plt.show()


if __name__ == '__main__':
    import sys
    if sys.argv[1] == 'create_plot':
        try:
            create_plot(app=sys.argv[2])
        except:
            print('Enter app name')
    elif sys.argv[1] == 'get_data':
        if len(sys.argv) == 2:
            get_apparat_data()
        else:
            get_apparat_data(app_name=sys.argv[2], need_graph=False)
