import socket
import sys
import time
import traceback
from threading import Thread

MyDict = {}
Unique_Values = set()
Terminate_all_Clients = False
Unique_Count = 0
Duplicate_Count = 0

def main():     
     start_server()


def start_server():    
    global Terminate_all_Clients
    host = "127.0.0.1"
    port = 4000         # arbitrary non-privileged port

    ######################################################
    # Open a file in write and Text mode.
    ######################################################
    FileH = open("numbers.log", "wt")


    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire
    print("Socket created")

    try:
        soc.bind((host, port))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()

    soc.listen(5)       # queue up to 5 requests
    print("Socket now listening")
    
    ######################################################
    #  Start book-keeping Thread
    ######################################################
    tb = Thread(target=BookKeeping_thread)
    tb.daemon = True
    tb.start()

    ######################################################
    #  Start ListenAndSpawn Thread
    ######################################################
    tb = Thread(target=ListenAndSpawn_thread, args=(soc,))
    tb.daemon = True
    tb.start()

    ######################################################
    #  As soon as we receive terminate from any client
    #  write out to the file, close the file and socket
    #  Exit out gracefully terminating all threads
    ######################################################
    while True:
        if(Terminate_all_Clients == True):
            #We have to shut down now and terminate all threads as well
            print("Terminate received")
            #Dump out the values to the output file and shut down            
            for keys in MyDict.keys():
                FileH.write('{}\n'.format(keys))
            FileH.close()
            soc.close()
            sys.exit()

##################################################################
#  ListenAndSpawn_thread accepts connections from client and 
#  spawn client thread that will perform the actual work
##################################################################
def ListenAndSpawn_thread(soc):
    # infinite loop- do not reset for every requests
    while True:
        connection, address = soc.accept()
        ip, port = str(address[0]), str(address[1])
        print("Connected with " + ip + ":" + port)
        try:
            tc = Thread(target=client_thread, args=(connection, ip, port))
            #t.daemon = True
            tc.start()
        except:
            print("Thread did not start.")
            traceback.print_exc()



########################################################################
#  BookKeeping_thread thread prints out the statistics every 10 seconds
########################################################################
def BookKeeping_thread():
    global Unique_Count
    global Duplicate_Count

    while True:
        print("Unique Count since last report: ", Unique_Count)
        print("Duplicate Count since last report: ", Duplicate_Count)
        print("Total Unique Count so far:", len(MyDict) )
        print("\n==========================================================\n")        
        time.sleep(10)
        

########################################################################
#  Client_thread reads data sent by the client and take necessary action
#  It calls other functions to process the data
########################################################################

def client_thread(connection, ip, port, max_buffer_size = 50):
    is_active = True

    print( "Started client thread")
    while is_active:
        client_input = receive_input(connection, max_buffer_size)

        if "terminate" in client_input:
            print("Client is requesting to terminate everything")  #Global flag set. Parent process will handle the full terminate
            connection.close()
            print("Connection " + ip + ":" + port + " closed")
            is_active = False            
        elif "--EXIT--" in client_input:
            is_active = False
            connection.sendall("-EXIT-".encode("ascii"))   #Send message to client to take quick exit
        else:
            print("Processed result: {}".format(client_input))
            connection.sendall("-".encode("ascii"))

########################################################################
#  receive_input receives data from the client. Will perform 
#  various validations and then call process_data to process the data
########################################################################
def receive_input(connection, max_buffer_size):
    global Terminate_all_Clients
    client_input = connection.recv(max_buffer_size)
    client_input_size = sys.getsizeof(client_input)

    #Check the validity of the incoming client data 
    # if not 9 characters, exit the Client
    num_characters = len(client_input)
    #print("client_input_size" ,num_characters)
    #print ("input is" , client_input)
    if num_characters != 9:
        print("number of characters sent were not 9. Terminate the client")
        return "--EXIT--"
    
    # if not digits, also exit the client
    if client_input.decode("ascii").rstrip().isdigit() != True:   
        if client_input.decode("ascii").rstrip() != "terminate":
            print("not terminate message and not digits so exit the client")
            return "--EXIT--"
     
    # if Terminate received, terminate all connections and shutdown the server
    if client_input.decode("ascii").rstrip() == "terminate":
        Terminate_all_Clients = True
        return("terminate")
    
    # Now process the data
    if client_input_size > max_buffer_size:
        print("The input size is greater than expected {}".format(client_input_size))

    decoded_input = client_input.decode("ascii").rstrip()  # decode and strip end of line
    result = process_data(decoded_input)

    return ("Success")   #successfully appeneded to the list

##########################################################################
#          process_data
##########################################################################

def process_data(input_str):
    global Unique_Count
    global Duplicate_Count

    #print("Processing the input received from client")

    # By this time, input must be 9 digits
    # Put them in a dictionary of key, value pair
    # where key is input digits and vallues is occurence count
    if input_str not in MyDict:
        Unique_Count += 1
        MyDict[input_str] = 1
    else:
        Duplicate_Count += 1
        MyDict[input_str] += 1
    
    #Also add it to set. Set data types preserves uniqueness
    Unique_Values.add(input_str)


if __name__ == "__main__":
    main()