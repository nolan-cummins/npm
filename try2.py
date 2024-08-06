from serial import *
import serial.tools.list_ports
import pygame, time
from pygame.locals import *

ports = sorted(serial.tools.list_ports.comports())
i = 1
print("\n")
for elem in ports:
  print(i, " - " + elem[0])
  i = i + 1
selectedPort = input("Select COM port option: ")
comPort = ports[int(selectedPort) - 1][0]

serialPort = Serial(comPort, 9600, timeout=0, writeTimeout=0)

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Arduino Communication')


while 1:
    if serialPort.in_waiting:
        readLetter = serialPort.read()
        #print(readLetter)

    for event in pygame.event.get():
        if (event.type == KEYUP):
            serialPort.write(b'%d1\n'%event.key);
            print('Keyup = %s'%pygame.key.name(event.key));
        if (event.type == KEYDOWN):
            serialPort.write(b'%d\n'%event.key);
            print('Keydown = %s'%pygame.key.name(event.key));
            print(event.key);
            #serialPort.write(b' ');
            time.sleep(5E-3)
            #print(serialPort.read());
            #print(serialPort.readline());
            #print(f'{event.key} the type of it is{type(event.key)}')
            if(event.key == K_1):
                print('Speed Setting 1')
            elif (event.key == K_2):
                print('Speed Setting 2')
            elif (event.key == K_3):
                print('Speed Setting 3')
            elif (event.key == K_4):
                print('Speed Setting 4')
            elif (event.key == K_5):
                print('Speed Setting 5')
            if(event.key == K_q):
                serialPort.close()
                pygame.quit()
                print("Loop ended")
                sys.exit()
                try: