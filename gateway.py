
import socket 
import time
import sys

GATEWAY_ADDRESS=8400
SERVER_ADDRESS=8004
DIM_BUFFER=1024 #BUFFER UTILIZZATO

server = ("localhost", SERVER_ADDRESS)
server_ip = "10.10.10.15"
server_mac = "10:35:35:38:70:F8"
gateway_address = ('gateway', GATEWAY_ADDRESS)

#ricezione dati (UDP)

counter=0

gateway_mac = "8F:E6:15:B1:42:75"
udp_gateway_ip="192.168.1.5"
tcp_gateway_ip="10.10.10.23"


while True:
    print("\n\n\n")
    counter+=1
    print("Giornata : %d"%(counter))
    print("\n\ngateway in attesa dei dati giornalieri delle 4 stazioni IOT")
    
    all_address=[] #array contenete gli indirizzi delle stazioni
    all_message=[] #array contente i dati delle stazioni
    
    # Creo il socket
    gateway = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # associo il socket alla porta
    gateway.bind(gateway_address)
    
    while True:
        print('\nAttendo il messaggio...')
        data, address=gateway.recvfrom(DIM_BUFFER)
        second_time=int(time.time()*1000000)
    
        if data:
        
            data1='Messaggio Ricevuto'
            time.sleep(2)
            sent=gateway.sendto(data1.encode(), address)
        
            data=data.decode('utf8')
            source_mac=data[0:17]
            destination_mac=data[17:34]
            source_ip=data[34:45]
            destination_ip=data[45:56]
            data=data[56:]
            
            for k in range(0, len(data)):#utilizzo lo slicing per individuare il tempo della partenza del pacchetto
                if data[k]=='+':
                    initial_time=data[k+1:]#salvo in una variabile il tempo 
                    data=data[:k]#così individuo il messaggio originale  e lo divido
                    break
            

    
            print("\nIl pacchetto ricevuto:\nSource MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
            print("Source IP address: {source_ip}, Destination IP address: {destination_ip}".format(source_ip=source_ip, destination_ip=destination_ip))
    
            
            
            final_time =second_time-int(initial_time)
            print('Tempo impiegato per trasmettere il pacchetto UDP è stato : %s ns'%(str(final_time)))
            print('\n')
                
        
            #aspetto i 4 messaggi poi chiudo la connesione
            if len(all_address)!=4 and address not in all_address:
                all_address.append(address)
                all_message.append(data)
            if len(all_address)==4:
                gateway.close()
                break
                    
                
        
    #invio dati al server (TCP)
                
    
                
  
    print('\nTutti i dati sono stati ricevuti. \nInvio al Server... \n')
        
    gateway = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    final_message=''
    try:
        gateway.connect(server)
    except Exception as data:
        print (Exception,":",data)
        print ("Non corretto")
        sys.exit(0)
    
    
    
    #raccolgo tutti i dati in un unica stringa
    for m in all_message:
        final_message+=m
        final_message+='\n'
    
    
    #Invio il messaggio finale
    time.sleep(2)

    t=int(time.time()*1000000)#calcolo il tempo in nano secondi trascorsi dal 01/01/1970
    final_message+='+'#aggiungo un carattere speciale
    final_message+=str(t)#aggiungo al messaggio il tempo all' invio del messaggio 
    
    ethernet_header = gateway_mac + server_mac
    IP_header = tcp_gateway_ip + server_ip
    packet = ethernet_header + IP_header + final_message
    
    
    
    gateway.send(packet.encode('utf8'))#invio...

    test = gateway.recv(1024)
    
    print (test.decode('utf8'))
    print('\n\n\n')

    
    gateway.close()


        
        
        
        
        
        
        



