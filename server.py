
from socket import *
import time

SERVER_ADDRESS=8004
DIM_BUFFER=1024 #BUFFER UTILIZZATO

server_ip = "10.10.10.15"
server_mac = "10:35:35:38:70:F8"
gateway_mac = "8F:E6:15:B1:42:75"

server = socket(AF_INET, SOCK_STREAM)
server_address=('localhost',SERVER_ADDRESS)
server.bind(server_address)
server.listen(1)

counter=0
while True:
    print("\n\n\n")
    counter+=1
    print("Giornata : %d"%(counter))
    print ('Server in ascolto ai dati in arrivo... \n')
    connection, addr=server.accept()

    try:

        received_message=connection.recv(DIM_BUFFER)
        second_time=int(time.time()*1000000)
        received_message=received_message.decode('utf8')
    
        source_mac = received_message[0:17]
        destination_mac = received_message[17:34]
        source_ip = received_message[34:45]
        destination_ip =  received_message[45:56]
        final_message = received_message[56:]
    
        print("\nIl pacchetto ricevuto:\nSource MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
        print("Source IP address: {source_ip}, Destination IP address: {destination_ip}".format(source_ip=source_ip, destination_ip=destination_ip))
    
        
        for k in range(0, len(final_message)):
            if final_message[k]=='+':
                initial_time=final_message[k+1:]
                final_message=final_message[:k]
                break
            
        final_time=second_time-int(initial_time)
        
        print("il messaggio è : ")
        print(final_message)
        print('Tempo impiegato per trasmettere il pacchetto TCP è stato : %s ns \n'%(str(final_time)))
        connection.send("I dati sono stati ricevuti".encode('utf8'))
        connection.close()
        
    except IOError:
 #Invia messaggio di risposta per file non trovato
        connection.send(bytes("HTTP/1.1 404 Not Found\r\n\r\n","UTF-8"))
        connection.send(bytes("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n","UTF-8"))
        connection.close()
        

