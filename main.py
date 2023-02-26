import threading
import socket
import time
from tkinter import *
from tkinter import ttk
import requestData

#####################################----MAIN----#########################################

#-------------------------------UPDATE_DATA_FUNCTION------------------------------------------
def update_data(cli):
    global checkDTC,checkINFO,errorCodes,vehicleVIN,vehicleECU
    
    newEngineLoad=requestData.Service01.engineLoad(cli)
    engineLoadProgress['value'] = newEngineLoad
    engineLoadProgressLabel.config(text='{}%'.format(newEngineLoad))

    newRPM=requestData.Service01.RPM(cli)
    rpmProgress['value'] = round(newRPM*100/16383.75,2)
    rpmProgressLabel.config(text=newRPM)
   
    newSpeed=requestData.Service01.speed(cli)
    speedLabel.config(text=newSpeed)
    
    newCoolant=requestData.Service01.coolantTemp(cli)
    coolantLabel.config(text='{}\N{DEGREE SIGN}C'.format(newCoolant))
    
    newthrottle=requestData.Service01.throttlePedalPosition(cli)
    throttleProgress['value'] = newthrottle
    throttleProgressLabel.config(text='{}%'.format(newthrottle))
    
    checkEngineStatus=requestData.Service01.statusMonitor(cli)
    if checkEngineStatus == 0:
        statusMonitorLabel.config(text='Check engine light: OFF')
        statusMonitorLabel1.config(text='Number of DTCs: 0')
    else:
        statusMonitorLabel.config(text='Check engine light: ON')
        statusMonitorLabel1.config(text='Number of DTCs: {}'.format(checkEngineStatus))
    
    if checkDTC == True:
        errorCodes=requestData.Service03.readDTC(cli)
        checkDTC= False

    if checkINFO == True:
        vehicleVIN=requestData.Service09.VIN(cli)
        vehicleECU=requestData.Service09.ECUName(cli)
        checkINFO = False

    time.sleep(1)
    update_data(cli)

#-------------------------------DTC_WINDOW------------------------------------------
def openDTCWindow():
    global errorCodes

    DTCwindow_width=200
    DTCwindow_height=400
    center_x = int(screen_width/2 - DTCwindow_width / 2)
    center_y = int(screen_height/2 - DTCwindow_height / 2)
    DTCwindow = Toplevel(gui)
    DTCwindow.title("Detected Error codes")
    DTCwindow.geometry('{}x{}+{}+{}'.format(DTCwindow_width, DTCwindow_height, center_x, center_y))
    DTCLabel0=Label(DTCwindow,text ="reading DTCs...")
    DTCLabel0.pack()
    if errorCodes==0:
        DTCLabel0.config(text='There are currently no DTCs')
    elif errorCodes==1:
        DTCLabel0.config(text='reading DTCs...')
    else:
        DTCLabel0.config(text='The following DTC were found:')
        for i in range(1,len(errorCodes)+1):
            Label(DTCwindow, text='{}'.format(errorCodes[i])).pack()

#-------------------------------DTC_WINDOW------------------------------------------
def openINFOWindow():
    global vehicleVIN, vehicleECU

    INFOwindow_width=400
    INFOwindow_height=200
    center_x = int(screen_width/2 - INFOwindow_width / 2)
    center_y = int(screen_height/2 - INFOwindow_height / 2)
    INFOwindow = Toplevel(gui)
    INFOwindow.title("Vehicle INFO")
    INFOwindow.geometry('{}x{}+{}+{}'.format(INFOwindow_width, INFOwindow_height, center_x, center_y))
    INFOLabel0=Label(INFOwindow,text ="waiting for vehicle info...")
    INFOLabel0.pack()
    if vehicleVIN==1:
        INFOLabel0.config(text ="waiting for vehicle info...")
    else:
        INFOLabel0.config(text='Vehicle VIN: {}'.format(vehicleVIN))
        Label(INFOwindow, text='Vehicle ECU: {}'.format(vehicleECU)).pack()

#-------------------------------CLOSE_GUI/CLIENT_FUNCTION--------------------------------------

def close_gui():
    gui.destroy()
    client.close()

#-------------------------------GLOBAL_VARIABLES------------------------------------------
checkDTC=True
checkINFO=True
errorCodes=1
vehicleECU=1
vehicleVIN=1
#-------------------------------CREATE_SOCKET------------------------------------------

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket Created')
CAR_IP= '127.0.0.1' # ELM327 TCP server IPS
CAR_PORT = 35000 # ELM327 port
# Connect the socket object to the ELM327 server
client.connect((CAR_IP,CAR_PORT))
print('Socket Connected to {}:{}'.format(CAR_IP, CAR_PORT))
print("-----------------------------------------")
print()

#-------------------------------GUI------------------------------------------
gui =Tk()
gui.title('OBD scanner')
gui.configure(bg='#171B26')
window_width = 1200
window_height =600
screen_width = gui.winfo_screenwidth()
screen_height = gui.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
gui.geometry('{}x{}+{}+{}'.format(window_width, window_height, center_x, center_y))
gui.resizable(False, False)
gui.protocol('WM_DELETE_WINDOW', close_gui)

gui.columnconfigure(0,weight=1, uniform='c')
gui.columnconfigure(1,weight=1, uniform='c')
gui.columnconfigure(2,weight=1, uniform='c')
gui.rowconfigure(0,weight=1, uniform='r')
gui.rowconfigure(1,weight=1, uniform='r')







#ENGINE LOAD GUI----------
engineloadFrame=Frame(gui,background='#171B26')
engineLoadLabel = Label(engineloadFrame,text = "Engine Load",bg='#171B26',fg='white',font =("Courier", 14, "bold")).pack()
engineLoadProgress = ttk.Progressbar(engineloadFrame,orient=HORIZONTAL, length=300, mode='determinate')
engineLoadProgress['value'] = 0
engineLoadProgress.pack()
engineLoadProgressLabel = Label(engineloadFrame, text = "waiting...",bg='#171B26',fg='white', font =("Courier", 14, "bold"))
engineLoadProgressLabel.pack()
engineloadFrame.grid(row=0, column=0, sticky=NSEW,pady=(100,0))

#SPEED GUI----------
speedFrame=Frame(gui,background='#171B26')
speedLabel = Label(speedFrame, text = "waiting...",bg='#171B26',fg='white', font =("Courier", 19, "bold"))
speedLabel.pack()
speedLabel2 = Label(speedFrame, text = "km/h",bg='#171B26',fg='white', font =("Courier", 14, "bold")).pack()
speedFrame.grid(row=0, column=1, sticky=NSEW,pady=(100,0))

#RPM GUI----------
rpmFrame=Frame(gui,background='#171B26')
rpmLabel = Label(rpmFrame, text = "RPM",bg='#171B26',fg='white',font =("Courier", 14, "bold")).pack()
rpmProgress = ttk.Progressbar(rpmFrame, orient=HORIZONTAL, length=300, mode='determinate')
rpmProgress['value'] = 0
rpmProgress.pack()
rpmProgressLabel = Label(rpmFrame,text = "waiting...",bg='#171B26',fg='white', font =("Courier", 14,"bold"))
rpmProgressLabel.pack()
rpmFrame.grid(row=0, column=2, sticky=NSEW,pady=(100,0))

#COOLANT_TEMP GUI----------
coolantTemp=Frame(gui,background='#171B26')
coolantLabel2 = Label(coolantTemp, text = "Coolant Temperature",bg='#171B26',fg='white', font =("Courier", 14, "bold")).pack()
coolantLabel = Label(coolantTemp,text = "waiting...",bg='#171B26',fg='white', font =("Courier", 19, "bold"))
coolantLabel.pack()
coolantTemp.grid(row=1, column=0, sticky=NSEW,pady=(30,0))

#THROTTLE_PEDAL_POSITION GUI----------
throttleFrame=Frame(gui,background='#171B26')
throttleLabel = Label(throttleFrame, text = "Throttle pedal position",bg='#171B26',fg='white', font =("Courier", 14, "bold")).pack()
throttleProgress = ttk.Progressbar(throttleFrame, orient=HORIZONTAL, length=300, mode='determinate')
throttleProgress['value'] = 0
throttleProgress.pack()
throttleProgressLabel = Label(throttleFrame, text = "waiting...",bg='#171B26',fg='white', font =("Courier", 14,"bold"))
throttleProgressLabel.pack()
throttleFrame.grid(row=1, column=1, sticky=NSEW,pady=(30,0))

#STATUS/ DTC----------
statusFrame=Frame(gui,background='#171B26')
statusMonitorLabel = Label(statusFrame, text = "Check engine light: waiting...",bg='#171B26',fg='white', font =("Courier", 14, "bold"))
statusMonitorLabel.pack()
statusMonitorLabel1 = Label(statusFrame, text = "Number of DTCs: waiting...",bg='#171B26',fg='white', font =("Courier", 14, "bold"))
statusMonitorLabel1.pack()
DTCbutton = Button(statusFrame, text="List all DTCs",font =("Courier", 14, "bold"),width=20, height=2, command=openDTCWindow).pack(pady=10)
vehicleInfoButton=Button(statusFrame, text="Show vehicle info",font =("Courier", 14, "bold"), width=20, height=2, command=openINFOWindow).pack(pady=10)
statusFrame.grid(row=1, column=2, sticky=NSEW,pady=(30,0))
#-----------------------------------
updateThread=threading.Thread(target=update_data, args=(client,))
updateThread.setDaemon(True)
updateThread.start()

#print()
#print(threading.active_count())
#print(threading.enumerate())

gui.mainloop()
