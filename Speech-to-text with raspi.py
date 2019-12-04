from RPLCD import CharLCD
from RPi import GPIO
from espeak import espeak
import RPi.GPIO as GPIO
import os
import speech_recognition as sr
import time
import mysql.connector

 

def send_data():
    db = mysql.connector.connect(user='username', password='password',
                              host='IP_address',
                              database='name of database')
    cur = db.cursor()
    nomeja="01"
    statusn="dipesan"
    
    try:
        cur.execute("INSERT INTO pesanan(Id_meja,pesanan,status)VALUES(%s,%s,%s)",(nomeja,hasil,statusn))
        db.commit()
    except:
        db.rollback()
        time.sleep(5)
    cur.close()
    db.close()

def button_delete(channel):
    print ("button pressed 21")
    lcd.clear()
    hasil=""
    os.system('aplay /home/pi/Downloads/pesanan_hapus.wav')

def button_send(ch):
    #print (hasil)
    lcd.clear()
    lcd.write_string(hasil)
    send_data()
    os.system('aplay /home/pi/Downloads/pesanan_terima.wav')

def record():
    with open('/home/pi/test.txt','w')as tulistest:
        tulistest.write("Pesanan anda adalah" +hasil)
    os.system('espeak -f "test.txt" -vid+f4 -s150 -w test.flac')
    os.system('aplay /home/pi/test.flac')
    
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
GPIO.add_event_detect(21, GPIO.FALLING, callback=button_delete)
GPIO.add_event_detect(19, GPIO.FALLING, callback=button_send)
lcd= CharLCD(numbering_mode=GPIO.BOARD, cols=20, rows=4, pin_rs=37, pin_e=35, pins_data=[40,38,36,32,33,31,29,23], dotsize=8, auto_linebreaks=True)
r= sr.Recognizer()
mic=sr.Microphone()

while True:
    
    with mic as source:
        try:
           
            audio=r.listen(source)
            hasil=r.recognize_google(audio, language='id-ID')
            print(hasil)
            lcd.clear()
            lcd.write_string(hasil)
            if(hasil=="menu"):
                lcd.clear()
                lcd.write_string("Selamat Mendengarkan Menu")
                os.system('aplay /home/pi/Downloads/menu.wav')
            else:
                record()
            
        except sr.UnknownValueError:
            print("coba ucapkan kembali")
            os.system('aplay /home/pi/Downloads/ulang.wav')
    
GPIO.cleanup()




