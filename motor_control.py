from gpiozero import AngularServo
from guizero import App, ButtonGroup, Text

app=App(title="Servo_GUI", layout="grid")
s = AngularServo(21, min_angle=-90, max_angle=90)
# s1 = AngularServo(23, min_angle=-90, max_angle=90)
# s2 = AngularServo(24, min_angle=-90, max_angle=90)
# s3 = AngularServo(4, min_angle=-90, max_angle=90)

def update_text():
    s.angle = int(choice.value)
    print("motor1: ", s.angle)
    # s1.angle = int(choice1.value)
    # print("motor2: ",s1.angle)
    # s2.angle = int(choice2.value)
    # print("motor3: ",s2.angle)
    # s3.angle = int(choice3.value)
    # print("motor4: ",s3.angle, "\n------------------------------------------------")

choice =ButtonGroup(app, options=["-90", "-45", "0", "45", "90"], selected="-90",command=update_text, grid=[1,2])
# choice1 =ButtonGroup(app, options=["-90", "-45", "0", "45", "90"], selected="-90", command=update_text, grid=[2,2])
# choice2 =ButtonGroup(app, options=["-90", "-45", "0", "45", "90"], selected="-90", command=update_text, grid=[3,2])
# choice3 =ButtonGroup(app, options=["-90", "-45", "0", "45", "90"], selected="-90", command=update_text, grid=[4,2])

Text(app, "M1",grid=[1,1])
# Text(app, "M2",grid=[2,1])
# Text(app, "M3",grid=[3,1])
# Text(app, "M4",grid=[4,1])
app.display()