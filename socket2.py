#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 14:38:11 2019

@author: martin
"""
import socket
import sys
import time
import serial


az_out = 0.00
el_out = 0.00
az_in = 0.00
el_in = 0.00

ser = serial.Serial()
#ser.port = "/dev/ttyUSB0"
ser.port = "/dev/ttyACM0"
#ser.port = "/dev/ttyS2"
ser.baudrate = 9800
ser.bytesize = serial.EIGHTBITS #number of bits per bytes
ser.parity = serial.PARITY_NONE #set parity check: no parity
ser.stopbits = serial.STOPBITS_ONE #number of stop bits
#ser.timeout = None          #block read
ser.timeout = 1            #non-block read
#ser.timeout = 2              #timeout block read
#ser.xonxoff = False     #disable software flow control
#ser.rtscts = False     #disable hardware (RTS/CTS) flow control
#ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
ser.writeTimeout = 2     #timeout for write







# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 4534)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    
    try:
        print >>sys.stderr, 'connection from', client_address
        #time.sleep(5)
        # Receive the data in small chunks and retransmit it
        while True:

            try: 
                ser.open()
            except Exception, e:
                print "error open serial port: " + str(e)
                exit()
            
            if ser.isOpen():
            
                try:
                    ser.flushInput() #flush input buffer, discarding all its contents
                    ser.flushOutput()#flush output buffer, aborting current output 
                    ser.write(bytes(b'W'))
                    print("write data:"+'W'.encode('utf-8'))
                    time.sleep(0.5)
                    response = ser.readline()
                    print("read data: " + response)
                    [az_out,el_out]=response.strip('\r\n').rsplit(' ')
                    
                    ser.flushInput()
                    ser.flushOutput()
                    ser.write(bytes(b'R '+str(az_in)+' '+str(el_in)))
                    print('write data:R '+str(az_in)+' '+str(el_in))
                    time.sleep(0.5)
                    response = ser.readline()
                    print("read data: " + response)
                    

		    ser.close()
                except Exception, e1:
                    print "error communicating...: " + str(e1)
            
            else:
                print "cannot open serial port "
                       
            

            data = connection.recv(16)
            print >>sys.stderr, 'received "%s"' % data
            
            if data[0] == 'P':
                az_in = float(data[1:7].replace(',', '.'))
                el_in = float(data[8:13].replace(',', '.'))

                #print >>sys.stderr, 'az_in' % az_in
                #print >>sys.stderr, 'el_in' % el_in
                connection.sendall('RPRT 0')
                count = 0

            
            if data[0] == 'p':
                data_out= str(az_out) + '\n' + str(el_out)
                connection.sendall(data_out)
                print >>sys.stderr, 'sending data back to the client'
                count = 0
            
            
            else:
                count += 1
                print >>sys.stderr, 'no more data from', client_address

            if count > 1:
                break
    

    
    finally:
        # Clean up the connection
        connection.close()
