
import timeoutTCP
import socket
from bitstring import BitArray

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#--------------------------------REQUESTDATA CLASS-----------------------------------------------------

class Service01:

    #RPM~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def RPM(c):
        # Create the message to receive RPM data
        RPMRequest = b'010C\r'
        #print('RPM request: {}'.format(RPMRequest))
        # Send the message to receive RPM data
        c.sendall(RPMRequest)

        # Receive the data from the vehicle
        RPMData = timeoutTCP.recv_timeout(c, 1)
        #print('Received RPM data (raw): {}'.format(RPMData))
        # Clean the data and convert it to string
        RPMData = RPMData.replace(RPMRequest, b'').replace(b' \r\r>', b'')
        RPMData = RPMData.decode('utf-8')
        #print('Decoded RPM data: {}'.format(RPMData))
        # Split the string into a list
        RPMParts = RPMData.split(' ')
        #print('RPM data parts: {}'.format(RPMParts))
        
        if len(RPMParts) != 4 or RPMParts[0] != '41' or RPMParts[1] != '0C':
             print('Invalid response RPM')
        else:
            # Calculate RPM
            rpm = (256 * int(RPMParts[2], 16) + int(RPMParts[3], 16)) / 4
            #print('{} RPM'.format(rpm))
            return rpm


    #SPEED~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def speed(c):
        SpeedRequest = b'010D\r'
        #print('Speed request: {}'.format(SpeedRequest))
        c.sendall(SpeedRequest)

        SpeedData = timeoutTCP.recv_timeout(c, 1)
        #print('Received Speed data (raw): {}'.format(SpeedData))
        SpeedData = SpeedData.replace(SpeedRequest, b'').replace(b' \r\r>', b'')
        SpeedData = SpeedData.decode('utf-8')
        #print('Decoded Speed data: {}'.format(SpeedData))
        SpeedParts = SpeedData.split(' ')
        #print('Speed data parts: {}'.format(SpeedParts))
       
        if len(SpeedParts) != 3 or SpeedParts[0] != '41' or SpeedParts[1] != '0D':
            print('Invalid response Speed')
        else:
            speed = int(SpeedParts[2], 16)
            #print('{} km/h'.format(speed))
            return speed

    #COOLANT_TEMP~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def coolantTemp(c):
        coolantTempRequest = b'0105\r'
        #print('coolantTemp request: {}'.format(coolantTempRequest))
        c.sendall(coolantTempRequest)

        coolantTempData = timeoutTCP.recv_timeout(c, 1)
        #print('Received coolantTemp data (raw): {}'.format(coolantTempData))
        coolantTempData = coolantTempData.replace(coolantTempRequest, b'').replace(b' \r\r>', b'')
        coolantTempData = coolantTempData.decode('utf-8')
        #print('Decoded coolantTemp data: {}'.format(coolantTempData))
        coolantTempParts = coolantTempData.split(' ')
        #print('coolantTemp data parts: {}'.format(coolantTempParts))
        
        if len(coolantTempParts) != 3 or coolantTempParts[0] != '41' or coolantTempParts[1] != '05':
            print('Invalid response Coolant Temp')
        else:
            coolantTemp = int(coolantTempParts[2], 16)-40
            #print('{} C'.format(coolantTemp))
            return coolantTemp


    #ENGINE_LOAD~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def engineLoad(c):
        engineLoadRequest = b'0104\r'
        #print('engineLoad request: {}'.format(engineLoadRequest))
        c.sendall(engineLoadRequest)

        engineLoadData = timeoutTCP.recv_timeout(c, 1)
        #print('Received engineLoad data (raw): {}'.format(engineLoadData))
        engineLoadData = engineLoadData.replace(engineLoadRequest, b'').replace(b' \r\r>', b'')
        engineLoadData = engineLoadData.decode('utf-8')
        #print('Decoded engineLoad data: {}'.format(engineLoadData))
        engineLoadParts = engineLoadData.split(' ')
        #print('engineLoad data parts: {}'.format(engineLoadParts))
        
        if len(engineLoadParts) != 3 or engineLoadParts[0] != '41' or engineLoadParts[1] != '04':
            print('Invalid response Engine Load')
        else:
            engineLoad = int(engineLoadParts[2], 16)/2.55
            #print('Engine load {} %'.format(round(engineLoad,2)))
            return round(engineLoad,2)


    #THROTTLE_PEDAL_POSITION~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def throttlePedalPosition(c):
        throttlePedalPositionRequest = b'0111\r'
        #print('throttlePedalPosition request: {}'.format(throttlePedalPositionRequest))
        c.sendall(throttlePedalPositionRequest)

        throttlePedalPositionData = timeoutTCP.recv_timeout(c, 1)
        
        #print('Received throttlePedalPosition data (raw): {}'.format(throttlePedalPositionData))
        throttlePedalPositionData = throttlePedalPositionData.replace(throttlePedalPositionRequest, b'').replace(b' \r\r>', b'')
        throttlePedalPositionData = throttlePedalPositionData.decode('utf-8')
        #print('Decoded throttlePedalPosition data: {}'.format(throttlePedalPositionData))
        throttlePedalPositionParts = throttlePedalPositionData.split(' ')
        #print('throttlePedalPosition data parts: {}'.format(throttlePedalPositionParts))
        
        if len(throttlePedalPositionParts) != 3 or throttlePedalPositionParts[0] != '41' or throttlePedalPositionParts[1] != '11':
            print('Invalid response Engine Load')
        else:
            throttlePedalPosition = int(throttlePedalPositionParts[2], 16)/2.55
            #print('Throttle pedal position {} %'.format(round(throttlePedalPosition, 2)))
            return round(throttlePedalPosition,2)

    #CHECK_ENGINE_LIGHT--STATUS_MONITOR~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def statusMonitor(c):
        statusMonitorRequest = b'0101\r'
        #print('Status request: {}'.format(statusMonitorRequest))
        c.sendall(statusMonitorRequest)
        statusMonitorData = timeoutTCP.recv_timeout(c, 1)
        #print('Received Status data (raw): {}'.format(statusMonitorData))
        statusMonitorData = statusMonitorData.replace(statusMonitorRequest, b'').replace(b' \r\r>', b'')
        statusMonitorData = statusMonitorData.decode('utf-8')
        statusMonitorData = statusMonitorData.split(' ')
        #print('Decoded Status data: {}'.format(statusMonitorData))
        statusMonitorbin=[]
        for i in range(0, 6):
            c = BitArray(hex=statusMonitorData[i])    
            statusMonitorbin.append(c)
        #print('binary Status data: {}'.format(statusMonitorbin))

        errorCode=statusMonitorbin[2]
        #print(errorCode)
        
        if errorCode[0]==0:
            return 0
        else:
            del errorCode[0:1]
            #print(errorCode)
            #print(int(errorCode.bin ,2))
            return(int(errorCode.bin ,2))
        
        

class Service03:

    def readDTC(c):
        DTCRequest = b'03\r'
        #print('DTC request: {}'.format(DTCClear))
        c.sendall(DTCRequest)

        DTCData = timeoutTCP.recv_timeout(c, 1)
        #print('DTC data (raw): {}'.format(DTCClear))
        DTCData = DTCData.replace(DTCRequest, b'').replace(b' \r\r>', b'')
        DTCData = DTCData.decode('utf-8')
        #print('Decoded engineLoad data: {}'.format(engineLoadData))
        DTCData = DTCData.split(' ')
        #print('engineLoad data parts: {}'.format(engineLoadParts))
        if DTCData[0] != '43' or DTCData[1] != '00':
            print('Invalid response DTC')
        elif len(DTCData)==2:
            #no DTCs
            return 0
        elif len(DTCData)>2:
            return DTCData

class Service09:

    def VIN(c):
        VINRequest = b'0902\r'
        #print('VIN request: {}'.format(VINRequest))
        c.sendall(VINRequest)

        VINData = timeoutTCP.recv_timeout(c, 1)
        #print('VIN data (raw): {}'.format(VINData))
        VINData = VINData.replace(VINRequest, b'').replace(b' \r\r>', b'').replace(b'014\r0: ', b'').replace(b' \r1:', b'').replace(b' \r2:', b'')
        VINData = VINData.decode('utf-8')
        #print('Decoded VIN data: {}'.format(VINData))
        VINParts = VINData.split(' ')
        #print('VIN data parts: {}'.format(VINParts))
        if VINParts[0] != '49' or VINParts[1] != '02':
            print('Invalid response VIN')
        else:
            VINnumber=""
            for i in range(3, len(VINParts)):
                VINnumber+=bytearray.fromhex(VINParts[i]).decode()
            return VINnumber
        
    def ECUName(c):
        ECUNameRequest = b'090A\r'
        #print('VIN request: {}'.format(VINRequest))
        c.sendall(ECUNameRequest)

        ECUNameData = timeoutTCP.recv_timeout(c, 1)
        #print('ECUName data (raw): {}'.format(ECUNameData))
        ECUNameData = ECUNameData.replace(ECUNameRequest, b'').replace(b' \r\r>', b'').replace(b'014\r0: ', b'').replace(b' \r00', b'').replace(b' \r65', b'').replace(b' \r6C', b'')
        ECUNameData = ECUNameData.decode('utf-8')
        #print('Decoded ECUName data: {}'.format(ECUNameData))
        ECUNameParts = ECUNameData.split(' ')
        #print('ECUName data parts: {}'.format(ECUNameParts))
        if ECUNameParts[1] != '49' or ECUNameParts[2] != '0A':
            print('Invalid response ECUName')
        else:
            ECU=""
            for i in range(4, len(ECUNameParts)):
                ECU+=bytearray.fromhex(ECUNameParts[i]).decode()
            return ECU

        