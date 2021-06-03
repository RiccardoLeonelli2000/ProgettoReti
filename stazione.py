# STAZIONE 1

import socket as sk
import time


def Stazione(message,ip,mac):
    
    gateway_mac="8F:E6:15:B1:42:75"
    udp_gateway_ip="192.168.1.5"

    DIM_BUFFER=1024

    client = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)   
    server_address = ('localhost', 8400)#server del gateway
    client.connect(server_address)
    

    try:

        # Invio il messaggio
        print('Invio dati : "%s" ' % message)
    
        t=int(time.time()*1000000)#calcolo il tempo in nano secondi trascorsi dal 01/01/1970
        message+='+'
        message+=str(t)
        
        ethernet_header = mac + gateway_mac
        IP_header = ip + udp_gateway_ip
        packet = ethernet_header + IP_header + message
    
        
        sent = client.sendto(packet.encode('utf8'), server_address)

        # Aspetto la risposta dal gateway
        print('Attendo la risposta dal gateway')
        data, server = client.recvfrom(DIM_BUFFER)
    
        print ('received message "%s"' % data.decode('utf8'))
        
    except Exception as info:
        print(info)
    finally:
        print ('closing socket')
        client.close()
        
