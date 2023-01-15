from tkinter import *
import random
import queue
import threading
import time
import json
import datetime
import sqlite3
from paho.mqtt import client as mqtt_client

broker 		= '0.tcp.ap.ngrok.io'
port 		= 13801
topic 		= "Jemuran"
client_id 	= f'python-mqtt-{random.randint(0, 100)}'

from paho.mqtt import client as mqtt_client

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

import json
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        _data = json.loads(msg.payload.decode())
        temp = _data['temp']
        hum = _data['hum']
        ldr = _data['ldr']
        position = _data['position']
    client.subscribe(topic)
    client.on_message = on_message



window = Tk()
window.title("Jemuran Pintar")
window.geometry('800x800') # Width, Height
window.resizable(False,False) # Width, Height
window.configure(bg="white")

# Banner image
canvas = Canvas(window, width=800,height=800)
canvas.place(x=0,y=0)
img = PhotoImage(file="Jemuran Pintar.png")
canvas.create_image(0,0,anchor=NW,image=img)


# Label °C dan % 1
tempC_label1 = Label(window, text="  °C", bg="white", fg="black", font=("Horta", 20))
tempC_label1.place(x=205,y=275)
moistP_label1 = Label(window, text="    %", bg="white", fg="black", font=("Horta", 20))
moistP_label1.place(x=515,y=275)
ldrS_label1 = Label(window, text="    lux", bg="white", fg="black", font=("Horta", 20))
ldrS_label1.place(x=205,y=600)
posP_label1 = Label(window, text="    °", bg="white", fg="black", font=("Horta", 20))
posP_label1.place(x=520,y=600)

# Label Temperature 
temp_label1 = Label(window,
                 text="",
                 bg="white",
                 fg="black",
                 font=("Horta", 20))

# Label Humadity 
hum_label1 = Label(window,
                 text="",
                 bg="white",
                 fg="black",
                 font=("Horta", 20))


# Label Photoresistor
ldr_label1 = Label(window,
                 text="",
                 bg="white",
                 fg="black",
                 font=("Horta", 20))

# Label Jemuran
position_label1 = Label(window,
                 text="",
                 bg="white",
                 fg="black",
                 font=("Horta", 20))


# DATABASE
current_time = datetime.datetime.now()

con = sqlite3.connect("database.sqlite", check_same_thread=False)
cur = con.cursor()

buat_tabel = '''CREATE TABLE IF NOT EXISTS JemuranTemp(
                        time TEXT NOT NULL,
                        jmrn_temp TEXT NOT NULL,
                        jmrn_hum TEXT NOT NULL,
                        jmrn_ldr TEXT NOT NULL,
                        jmrn_position TEXT NOT NULL,
                        );'''
try:
    cur.execute(buat_tabel)
    con.commit()
    print("Table created successfully")
except Exception as e:
    print("Error creating table:", e)
    con.rollback()

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        
        global temp_label1
        global hum_label1
        global ldr_label1
        global position_label1

        try:
            _data = json.loads(msg.payload.decode())
            
            temp = str(_data["temp"])
            temp_label1.place(x=185,y=275, anchor=NW)
            temp_label1.config(text=temp)

            hum = str(_data["hum"])
            hum_label1.place(x=500,y=275, anchor=NW)
            hum_label1.config(text=hum)
            
            ldr = str(_data["ldr"])
            ldr_label1.place(x=185,y=600, anchor=NW)
            ldr_label1.config(text=ldr)

            position = str(_data["position"])
            position_label1.place(x=500,y=600, anchor=NW)
            position_label1.config(text=position)

            data_sensor_val = (temp, hum, ldr, position)
            cur.execute(
                "INSERT INTO JemuranTemp ('time',temp11, hum11, ldr11, psoition11) VALUES ('{}',?,?,?);".format(current_time), data_sensor_val)
            con.commit()
            
        except Exception as e:
            print("Data berhasil dimuat !")

    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()
    time.sleep(1)  # add delay here
    window.mainloop()
    client.loop_stop()

if __name__ == '__main__':
    run()
