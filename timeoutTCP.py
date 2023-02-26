

#--------------------------------TCP READ WITH TIMEOUT FUNCTION-----------------------------------------------------
import time

# Define the recv_timeout function with a default timeout of 2s
def recv_timeout(the_socket,timeout=2):
    # Make socket non blocking
    the_socket.setblocking(False)
 
    # Total data partwise in a list
    total_data = []
 
    # Beginning time
    begin = time.time()
    while True:
        # If you got some data, then break after timeout
        if total_data and time.time() - begin > timeout:
            break
 
        # If you got no data at all, wait longer, twice the timeout
        elif time.time() - begin > timeout * 2:
            break
 
         # Receive something
        try:
            data = the_socket.recv(8192)
            if data:
                total_data.append(data)
                # Change the beginning time for measurement
                begin = time.time()
            else:
                # Sleep for some time to indicate a gap
                time.sleep(0.1)
        except Exception as e:
            # print(e)
            pass
 
    # Join all parts in the list to make final bytes string
    return b''.join(total_data)