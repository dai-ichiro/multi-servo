import serial, time
from decimal import Decimal, ROUND_HALF_UP

with open('motion.txt') as f:
    lines = [s.strip() for s in f.readlines()[1:]]

print("Open Port")
ser =serial.Serial("COM6", 9600)
time.sleep(2)

#servoは201からカウントすることとする
#servoの角度は0～179
#サーボ番号と角度がバッティングすることはない
servo_1_id = (201).to_bytes(1, 'big')
servo_2_id = (202).to_bytes(1, 'big')
servo_3_id = (203).to_bytes(1, 'big')
servo_4_id = (204).to_bytes(1, 'big')

servo_1_previous = 90
servo_2_previous = 90
servo_3_previous = 90
servo_4_previous = 90

for i in range(len(lines)):
    
    x = lines[i].split()
    
    x = [int(i) for i in x]
    x = [179 if i > 179 else i for i in x]
    x = [0 if i < 0 else i for i in x]

    times = x[4]

    for i in range(times + 1):
        servo1 = servo_1_previous + ((x[0]-servo_1_previous)/times) * i
        servo2 = servo_2_previous + ((x[1]-servo_2_previous)/times) * i
        servo3 = servo_3_previous + ((x[2]-servo_3_previous)/times) * i
        servo4 = servo_4_previous + ((x[3]-servo_4_previous)/times) * i

        servo1 = int(Decimal(str(servo1)).quantize(Decimal('0'), rounding=ROUND_HALF_UP))
        servo2 = int(Decimal(str(servo2)).quantize(Decimal('0'), rounding=ROUND_HALF_UP))
        servo3 = int(Decimal(str(servo3)).quantize(Decimal('0'), rounding=ROUND_HALF_UP))
        servo4 = int(Decimal(str(servo4)).quantize(Decimal('0'), rounding=ROUND_HALF_UP))

        servo_1_angle = (servo1).to_bytes(1, 'big')
        servo_2_angle = (servo2).to_bytes(1, 'big')
        servo_3_angle = (servo3).to_bytes(1, 'big')
        servo_4_angle = (servo4).to_bytes(1, 'big')

        ser.write(servo_1_id)
        ser.write(servo_1_angle)
        
        ser.write(servo_2_id)
        ser.write(servo_2_angle)

        ser.write(servo_3_id)
        ser.write(servo_3_angle)

        ser.write(servo_4_id)
        ser.write(servo_4_angle)

        finished = False
        while not finished:
            finished = (ser.in_waiting > 0)
        ser.reset_input_buffer()

    print('one motion send')

    servo_1_previous = servo1
    servo_2_previous = servo2
    servo_3_previous = servo3
    servo_4_previous = servo4

print("Close Port")
ser.close()