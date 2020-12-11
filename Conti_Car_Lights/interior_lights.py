from PyQt4 import QtCore, QtGui, QtTest

import time
import threading

spinbox_value = 0
last_percentage_value = 0
stop_all = False

class ThreadClass(QtCore.QThread):
    def init(self, parent = None):
        super(ThreadClass, self).init(parent)

    def run(self):
        self.emit(QtCore.SIGNAL('FADE_IN'), spinbox_value)
        self.emit(QtCore.SIGNAL('FADE_OUT'), spinbox_value)

class Ui_MainWindow(object):
    threadClass = ThreadClass()
    interior_led_state = False
    stop_event = False

    max_left_door_value = 0
    max_right_door_value = 0

    warning_pressed = 0
    left_turn_pressed = 0
    left_turn_resumed = 0
    right_turn_pressed = 0
    right_turn_resumed = 0
    carlight_pressed = 0

    KL_list_index = 0
    KL_list = ["No", "s", "15", "50", "75"]

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(900, 500)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        MainWindow.setCentralWidget(self.centralwidget)

        # Set background application color
        self.centralwidget.setStyleSheet("background-color: white;")

        # Continental image
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(5, 350, 350, 120))
        pixmap = QtGui.QPixmap("conti.png")
        pixmap = pixmap.scaled(350, 120, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap)

        # Car image
        self.label_1 = QtGui.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(300, 170, 331, 161))
        pixmap1 = QtGui.QPixmap("car.jpg")
        pixmap1 = pixmap1.scaled(331, 161, QtCore.Qt.KeepAspectRatio)
        self.label_1.setPixmap(pixmap1)

        # Left door button
        self.left_door = QtGui.QPushButton(MainWindow)
        self.left_door.setText("Left Door")
        self.left_door.setStyleSheet("font: bold;")
        self.left_door.setGeometry(QtCore.QRect(380, 50, 211, 41))
        self.left_door.clicked.connect(self.fade_door_left)

        # Left door slider
        self.left_door_slider = QtGui.QSlider(self.centralwidget)
        self.left_door_slider.setGeometry(QtCore.QRect(410, 100, 160, 26))
        self.left_door_slider.setOrientation(QtCore.Qt.Horizontal)
        self.left_door_slider.setRange(0, 100)
        self.left_door_slider.setValue(0)
        self.left_door_slider.valueChanged.connect(self.valuechange_left_slider)

        # Left door spinbox
        self.spinBox_left = QtGui.QSpinBox(MainWindow)
        self.spinBox_left.setGeometry(QtCore.QRect(300, 50, 75, 41))
        self.spinBox_left.setKeyboardTracking(True)
        self.spinBox_left.setRange(0, 100)
        self.spinBox_left.valueChanged.connect(self.valuechange)

        # Right door
        self.right_door = QtGui.QPushButton(MainWindow)
        self.right_door.setText("Right door")
        self.right_door.setStyleSheet("font: bold;")
        self.right_door.setGeometry(QtCore.QRect(380, 400, 211, 41))
        self.right_door.clicked.connect(self.fade_door_right)

        # Right door slider
        self.right_door_slider = QtGui.QSlider(self.centralwidget)
        self.right_door_slider.setGeometry(QtCore.QRect(410, 360, 160, 26))
        self.right_door_slider.setOrientation(QtCore.Qt.Horizontal)
        self.right_door_slider.setRange(0, 100)
        self.right_door_slider.setValue(0)
        self.right_door_slider.valueChanged.connect(self.valuechange_right_slider)

        # Right door spinbox
        self.spinBox_right = QtGui.QSpinBox(MainWindow)
        self.spinBox_right.setGeometry(QtCore.QRect(300, 400, 75, 41))
        self.spinBox_right.setKeyboardTracking(False)
        self.spinBox_right.setRange(0, 100)
        self.spinBox_right.valueChanged.connect(self.valuechange)

        # Current kl label
        self.current_kl_label = QtGui.QLabel(self.centralwidget)
        self.current_kl_label.setGeometry(QtCore.QRect(680, 80, 151, 31))
        self.current_kl_label.setStyleSheet("font: bold;")
        self.current_kl_label.setText("Current KL: no_KL")

        # Previous kl button
        self.prev_kl = QtGui.QPushButton(MainWindow)
        self.prev_kl.setText("Previous KL")
        self.prev_kl.setStyleSheet("font: bold;")
        self.prev_kl.setGeometry(QtCore.QRect(670, 40, 101, 31))
        self.prev_kl.clicked.connect(self.prev_kl_function)
        self.prev_kl.setEnabled(False)

        # Prev kl label
        self.prev_kl_label = QtGui.QLabel(self.centralwidget)
        self.prev_kl_label.setGeometry(QtCore.QRect(780, 40, 92, 31))
        self.prev_kl_label.setStyleSheet("font: bold;")

        # Next kl button
        self.next_kl = QtGui.QPushButton(MainWindow)
        self.next_kl.setText("Next KL")
        self.next_kl.setStyleSheet("font: bold;")
        self.next_kl.setGeometry(QtCore.QRect(670, 120, 101, 31))
        self.next_kl.clicked.connect(self.next_kl_function)

        # Next kl label
        self.next_kl_label = QtGui.QLabel(self.centralwidget)
        self.next_kl_label.setGeometry(QtCore.QRect(780, 120, 81, 31))
        self.next_kl_label.setStyleSheet("font: bold;")
        self.next_kl_label.setText("KL_s")

        # green led for interior lights
        self.interiorLightsLabel = QtGui.QLabel(self.centralwidget)
        self.interiorLightsLabel.setGeometry(QtCore.QRect(220, 160, 20, 20))

        # inside carLight Button
        self.carLight1 = QtGui.QPushButton(MainWindow)
        self.carLight1.setText("Car Light")
        self.carLight1.setStyleSheet("font: bold;")
        self.carLight1.setGeometry(QtCore.QRect(680, 230, 120, 41))
        self.carLight1.clicked.connect(self.carLight)

        # inside carLight
        self.carLight = QtGui.QLabel(self.centralwidget)
        self.carLight.setGeometry(QtCore.QRect(450, 240, 20, 20))

        # warning Lights Button
        self.warning = QtGui.QPushButton(MainWindow)
        self.warning.setText("Warning Lights")
        self.warning.setStyleSheet("font: bold;")
        self.warning.setGeometry(QtCore.QRect(50, 100, 160, 41))
        self.warning.clicked.connect(self.warningLightsButton)

        # left signaling Button
        self.warningLeft = QtGui.QPushButton(MainWindow)
        self.warningLeft.setText("Left Signaling")
        self.warningLeft.setStyleSheet("font:bold;")
        self.warningLeft.setGeometry(QtCore.QRect(680, 350, 120, 41))
        self.warningLeft.clicked.connect(self.leftSignaling)

        # right signaling Button
        self.warningRight = QtGui.QPushButton(MainWindow)
        self.warningRight.setText("Right Signaling")
        self.warningRight.setStyleSheet("font:bold;")
        self.warningRight.setGeometry(QtCore.QRect(680, 390, 120, 41))
        self.warningRight.clicked.connect(self.rightSignaling)

        # Warning Lights
        self.warningLight1 = QtGui.QLabel(self.centralwidget)
        self.warningLight1.setGeometry(QtCore.QRect(260, 190, 20, 20))

        self.warningLight2 = QtGui.QLabel(self.centralwidget)
        self.warningLight2.setGeometry(QtCore.QRect(260, 293, 20, 20))

        self.warningLight3 = QtGui.QLabel(self.centralwidget)
        self.warningLight3.setGeometry(QtCore.QRect(650, 190, 20, 20))

        self.warningLight4 = QtGui.QLabel(self.centralwidget)
        self.warningLight4.setGeometry(QtCore.QRect(650, 293, 20, 20))

        # Lock Car
        self.lockCar1 = QtGui.QPushButton(MainWindow)
        self.lockCar1.setText("Lock car")
        self.lockCar1.setStyleSheet("font: bold;")
        self.lockCar1.setGeometry(QtCore.QRect(680, 310, 120, 41))
        self.lockCar1.clicked.connect(self.LockCar)

        # Unlock Car
        self.unlockCar1 = QtGui.QPushButton(MainWindow)
        self.unlockCar1.setText("Unlock car")
        self.unlockCar1.setStyleSheet("font: bold;")
        self.unlockCar1.setGeometry(QtCore.QRect(680, 270, 120, 41))
        self.unlockCar1.clicked.connect(self.unlockCar)

        # 4 leds for sweep
        self.led1_sweep = QtGui.QLabel(self.centralwidget)
        self.led1_sweep.setGeometry(QtCore.QRect(220, 210, 20, 20))

        self.led2_sweep = QtGui.QLabel(self.centralwidget)
        self.led2_sweep.setGeometry(QtCore.QRect(240, 210, 20, 20))

        self.led3_sweep = QtGui.QLabel(self.centralwidget)
        self.led3_sweep.setGeometry(QtCore.QRect(260, 210, 20, 20))

        self.led4_sweep = QtGui.QLabel(self.centralwidget)
        self.led4_sweep.setGeometry(QtCore.QRect(280, 210, 20, 20))

        # KL_s led
        self.KL_S = QtGui.QLabel(self.centralwidget)
        self.KL_S.setGeometry(QtCore.QRect(806, 230, 20, 20))

        # KL_15 led
        self.KL_15 = QtGui.QLabel(self.centralwidget)
        self.KL_15.setGeometry(QtCore.QRect(806, 255, 20, 20))

        # KL_50 led
        self.KL_50 = QtGui.QLabel(self.centralwidget)
        self.KL_50.setGeometry(QtCore.QRect(806, 280, 20, 20))

        # KL_75 led
        self.KL_75 = QtGui.QLabel(self.centralwidget)
        self.KL_75.setGeometry(QtCore.QRect(806, 305, 20, 20))

        # Left door led
        self.left_door_led = QtGui.QLabel(self.centralwidget)
        self.left_door_led.setGeometry(QtCore.QRect(600, 60, 20, 20))

        # Right door led
        self.right_door_led = QtGui.QLabel(self.centralwidget)
        self.right_door_led.setGeometry(QtCore.QRect(600, 410, 20, 20))

        # Close all leds button
        self.close_all = QtGui.QPushButton(MainWindow)
        self.close_all.setText("Close all leds")
        self.close_all.setStyleSheet("font: bold;color: red")
        self.close_all.setGeometry(QtCore.QRect(50, 50, 120, 35))
        self.close_all.clicked.connect(self.close_all_leds)

        # 1 Led inside
        self.interior_lights = QtGui.QPushButton(MainWindow)
        self.interior_lights.setText("Interior lights")
        self.interior_lights.setStyleSheet("font: bold;")
        self.interior_lights.setGeometry(QtCore.QRect(50, 150, 160, 41))
        self.interior_lights.clicked.connect(self.set_interior_lights)

        # Led brightness percentage label
        self.percentage_label = QtGui.QLabel(self.centralwidget)
        self.percentage_label.setGeometry(QtCore.QRect(50, 260, 90, 40))
        self.percentage_label.setStyleSheet("font: bold;")
        self.percentage_label.setText("Percentage")

        # Led brightness progress bar
        self.progress_bar = QtGui.QProgressBar(MainWindow)
        self.progress_bar.setGeometry(50, 310, 200, 21)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        # Led brightness spinbox
        self.spinBox = QtGui.QSpinBox(MainWindow)
        self.spinBox.setGeometry(QtCore.QRect(150, 260, 75, 41))
        self.spinBox.setKeyboardTracking(False)
        self.spinBox.setRange(0, 100)
        self.spinBox.valueChanged.connect(self.start_thread)
        self.spinBox.valueChanged.connect(self.valuechange)

        # Sweep button
        self.sweep = QtGui.QPushButton(MainWindow)
        self.sweep.setText("Sweep")
        self.sweep.setStyleSheet("font: bold;")
        self.sweep.setGeometry(QtCore.QRect(50, 200, 160, 41))
        self.sweep.clicked.connect(self.sweep_threads)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.show()

    ############################### EXERCISE 1 ###############################
    # Clear all leds and widgtets when the Close all leds is pressed
    def close_all_leds(self):
        self.carLight.setStyleSheet("background-color:white;border-radius:5px;")
        self.warningLight1.setStyleSheet("background-color:white;border-radius:5px;")
        self.warningLight2.setStyleSheet("background-color:white;border-radius:5px;")
        self.warningLight3.setStyleSheet("background-color:white;border-radius:5px;")
        self.warningLight4.setStyleSheet("background-color:white;border-radius:5px;")

        self.led1_sweep.setStyleSheet("background-color:white;border-radius:5px;")
        self.led2_sweep.setStyleSheet("background-color:white;border-radius:5px;")
        self.led3_sweep.setStyleSheet("background-color:white;border-radius:5px;")
        self.led4_sweep.setStyleSheet("background-color:white;border-radius:5px;")

        self.interiorLightsLabel.setStyleSheet("background-color:white;border-radius:5px;")
        self.KL_S.setStyleSheet("background-color:white;border-radius:5px;")
        self.KL_15.setStyleSheet("background-color:white;border-radius:5px;")
        self.KL_50.setStyleSheet("background-color:white;border-radius:5px;")
        self.KL_75.setStyleSheet("background-color:white;border-radius:5px;")

        self.progress_bar.setValue(0)
        self.spinBox.setValue(0)
        
        global stop_all
        stop_all = True

        self.interior_led_state = False
        self.stop_event = True

        self.warning_pressed = 0
        self.left_turn_pressed = 0
        self.right_turn_pressed = 0
        self.carlight_pressed = 0

    # Open one led when interior lights is pressed
    def interior_light_led(self, b1):
        self.interiorLightsLabel.setStyleSheet("background-color:" + str(b1) + ";border-radius:5px;")

    # Function called from button handler
    def set_interior_lights(self):
        if not self.interior_led_state:
            self.interior_light_led("green")
            self.interior_led_state = True
        else:
            self.interior_light_led("white")
            self.interiorLightsLabel.setText("")
            self.interior_led_state = False

    ############################### EXERCISE 2 ###############################
    # Sweep Leds thread
    def sweep_threads(self):
        stop_event = threading.Event()
        sweepThread = threading.Thread(target=self.sweep_leds, args=(stop_event,))
        sweepThread.daemon = True
        sweepThread.start()

    # Sweep Leds function
    def sweep_leds(self, stop_event):
        self.set4leds("orange", "white", "white", "white")
        time.sleep(1)
        self.set4leds("orange", "orange", "white", "white")
        time.sleep(1)
        self.set4leds("orange", "orange", "orange", "white")
        time.sleep(1)
        self.set4leds("orange", "orange", "orange", "orange")
        
    # Sweep Leds
    def set4leds(self, led1, led2, led3, led4):
        self.led1_sweep.setStyleSheet("background-color:" + str(led1) + ";border-radius:5px;")
        self.led2_sweep.setStyleSheet("background-color:" + str(led2) + ";border-radius:5px;")
        self.led3_sweep.setStyleSheet("background-color:" + str(led3) + ";border-radius:5px;")
        self.led4_sweep.setStyleSheet("background-color:" + str(led4) + ";border-radius:5px;")

    ############################### EXERCISE 3 ###############################
    # Change progress bar value when spinbox value is changed
    def valuechange(self): 
        global spinbox_value
        global last_percentage_value
        spinbox_value = self.spinBox.value()
        if self.spinBox.value() > last_percentage_value:
            self.threadClass.start()
            self.threadClass.connect(self.threadClass, QtCore.SIGNAL('FADE_IN'), self.change_pb_up_value)
        else:
            self.threadClass.start()
            self.threadClass.connect(self.threadClass, QtCore.SIGNAL('FADE_OUT'), self.change_pb_down_value)
        self.progress_bar.setValue(self.spinBox.value())
        last_percentage_value = spinbox_value

    # Change led brightness up when the spinbox value (representing led brightness percentage) is bigger than progress bar value 
    def change_pb_up_value(self, value):
        self.percentage_label.setStyleSheet("background-color:rgba(110,100,110," + str(value/100) + ");border-radius:5px;")

    # Change led brightness down when the spinbox value (representing led brightness percentage) is less than progress bar value 
    def change_pb_down_value(self, value):
        self.percentage_label.setStyleSheet("background-color:rgba(110,100,110," + str(value/100) + ");border-radius:5px;")

    def start_thread(self):
        self.threadClass.start()

    ############################### EXERCISE 4 ###############################
    # Succesice KL led turn
    def KL_lights(self, KL):

        # !!! TODO:
        #  culori la fiecare led pentru KL
        if KL == "No":
            self.set_bg_colors("white", "white", "white", "white")
        if KL == "s":
            self.set_bg_colors("lightgray", "white", "white", "white")
        if KL == "15":
            self.set_bg_colors("lightgray", "green", "white", "white")
        if KL == "50":
            self.set_bg_colors("lightgray", "green", "red", "white")
        if KL == "75":
            self.set_bg_colors("lightgray", "green", "red", "blue")

    # Set previous value for KL when previous KL button is pressed
    def prev_kl_function(self):
        self.set_enable("next", True)

        if self.KL_list_index == 0:
            self.current_kl_label.setText("Current KL: No KL")

        if self.KL_list_index > 0:
            self.KL_list_index -= 1
            self.current_kl_label.setText("Current KL: KL_" + self.KL_list[self.KL_list_index])
            if self.KL_list_index - 1 == -1:
                self.set_enable("prev", False)

        self.next_kl_label.setText("KL_" + self.KL_list[self.KL_list_index + 1])
        self.KL_lights(self.KL_list[self.KL_list_index])

    # Set next value for KL when next KL button is pressed
    def next_kl_function(self):
        self.set_enable("prev", True)

        if self.KL_list_index == 4:
            self.current_kl_label.setText("Current KL: KL_75")

        if self.KL_list_index < 4:
            self.KL_list_index += 1
            self.current_kl_label.setText("Current KL: KL_" + self.KL_list[self.KL_list_index])
            if self.KL_list_index + 1 == 5:
                self.next_kl_label.setText("None")
            else:
                self.next_kl_label.setText("KL_" + self.KL_list[self.KL_list_index + 1])
            if self.KL_list_index == 4:
                self.set_enable("next", False)

        self.KL_lights(self.KL_list[self.KL_list_index])

    # Set enable KL buttons
    def set_enable(self, button, value):
        #print(value)
        #print(type(value))
        if button == "prev":
            self.prev_kl.setEnabled(value)
        if button == "next":
            self.next_kl.setEnabled(value)

    # Set KL leds colors
    def set_bg_colors(self, l1, l2, l3, l4):
        self.KL_S.setStyleSheet("background-color:" + str(l1) + ";border-radius:5px;")
        self.KL_15.setStyleSheet("background-color:" + str(l2) + ";border-radius:5px;")
        self.KL_50.setStyleSheet("background-color:" + str(l3) + ";border-radius:5px;")
        self.KL_75.setStyleSheet("background-color:" + str(l4) + ";border-radius:5px;")

    ############################### EXERCISE 5 ##############################
    ################################ BONUS ################################
    # Open left door untill the obstacle is detected
    def fade_door_left(self):
        value = self.spinBox_left.value()
        self.left_door_slider.setValue(value)
        self.max_left_door_value = value
        self.left_door_slider.setSliderPosition(value)

    # Fade out left door led brightness when slider is moving under obstacle value
    def valuechange_left_slider(self):
        value = self.left_door_slider.value()
    
        if value >= self.max_left_door_value:
            self.left_door_slider.setSliderPosition(self.max_left_door_value)
            self.left_door_led.setStyleSheet("background-color: red;border-radius:5px;")
        elif value >= self.max_left_door_value - 10 and value < self.max_left_door_value:
            self.left_door_led.setStyleSheet("background-color: orange;border-radius:5px;")
        elif value >= int(self.max_left_door_value / 2) and value < self.max_left_door_value:
            self.left_door_led.setStyleSheet("background-color: yellow;border-radius:5px;")
        elif value < int(self.max_left_door_value / 2):
            self.left_door_led.setStyleSheet("background-color: green;border-radius:5px;")


    # Open right door untill the obstacle is detected
    def fade_door_right(self):
        value = self.spinBox_right.value()
        self.right_door_slider.setValue(value)
        self.max_right_door_value = value
        self.right_door_slider.setSliderPosition(value)

    # Fade out right door led brightness when slider is moving under obstacle value
    def valuechange_right_slider(self):
        value = self.right_door_slider.value()
    
        if value >= self.max_right_door_value:
            self.right_door_slider.setSliderPosition(self.max_right_door_value)
            self.right_door_led.setStyleSheet("background-color: red;border-radius:5px;")
        elif value >= self.max_right_door_value - 10 and value < self.max_right_door_value:
            self.right_door_led.setStyleSheet("background-color: orange;border-radius:5px;")
        elif value >= int(self.max_right_door_value / 2) and value < self.max_right_door_value:
            self.right_door_led.setStyleSheet("background-color: yellow;border-radius:5px;")
        elif value < int(self.max_right_door_value / 2):
            self.right_door_led.setStyleSheet("background-color: green;border-radius:5px;")

    #########################################################################
    ############################### USED FUNCTION ###########################
    def setWarningLights(self, warningLight1, warningLight2, warningLight3, warningLight4):
        self.warningLight1.setStyleSheet("background-color:" + str(warningLight1) + ";border-radius:5px;")
        self.warningLight2.setStyleSheet("background-color:" + str(warningLight2) + ";border-radius:5px;")
        self.warningLight3.setStyleSheet("background-color:" + str(warningLight3) + ";border-radius:5px;")
        self.warningLight4.setStyleSheet("background-color:" + str(warningLight4) + ";border-radius:5px;")

    #########################################################################

    ############################### EXERCISE 6 ##############################
    # Warning lights thread
    def warningLightsButton(self):

        if self.warning_pressed == 0:
            self.warning_pressed = 1
        elif self.warning_pressed == 1:
            self.warning_pressed = 0
        
        if self.left_turn_pressed == 1:
            self.left_turn_pressed = 0

        if self.right_turn_pressed == 1:
            self.right_turn_pressed = 0

        stop_event = threading.Event()
        warningThread = threading.Thread(target=self.whileLights, args=(stop_event,))
        warningThread.daemon = True
        warningThread.start()

    # Warning Lights function
    def whileLights(self, stop_event):
        while self.warning_pressed == 1:
            self.setWarningLights("orange", "orange", "orange", "orange")
            time.sleep(1)
            self.setWarningLights("white", "white", "white", "white")
            time.sleep(1)
        if self.warning_pressed == 0:
            self.setWarningLights("white", "white", "white", "white")


    ############################### EXERCISE 7 ##############################
    # Left Signaling Lights
    def leftSignaling(self):

        if self.warning_pressed == 1:
            self.warning_pressed = 0
        
        if self.left_turn_pressed == 0:
            self.left_turn_pressed = 1
        elif self.left_turn_pressed == 1:
            self.left_turn_pressed = 0

        if self.right_turn_pressed == 1:
            self.right_turn_pressed = 0

        stop_event = threading.Event()
        left_thread = threading.Thread(target=self.whileLeft, args=(stop_event,))
        left_thread.daemon = True
        left_thread.start()

    def whileLeft(self, stop_event):
        while self.left_turn_pressed == 1:
            self.setWarningLights("orange", "white", "orange", "white")
            time.sleep(1)
            self.setWarningLights("white", "white", "white", "white")
            time.sleep(1)
        if self.left_turn_pressed == 0:
            self.setWarningLights("white", "white", "white", "white")
            

    ############################### EXERCISE 8 ##############################
    # Right Signaling Lights
    def rightSignaling(self):

        if self.warning_pressed == 1:
            self.warning_pressed = 0
        
        if self.left_turn_pressed == 1:
            self.left_turn_pressed = 0

        if self.right_turn_pressed == 1:
            self.right_turn_pressed = 0
        elif self.right_turn_pressed == 0:
            self.right_turn_pressed = 1

        stop_event = threading.Event()
        right_thread = threading.Thread(target=self.whileRight, args=(stop_event,))
        right_thread.daemon = True
        right_thread.start()

    def whileRight(self, stop_event):
        while self.right_turn_pressed == 1:
            self.setWarningLights("white", "orange", "white", "orange")
            time.sleep(1)
            self.setWarningLights("white", "white", "white", "white")
            time.sleep(1)
        if self.right_turn_pressed == 0:
            self.setWarningLights("white", "white", "white", "white")

    ############################### EXERCISE 9 ##############################
    def setcarLight(self, color):
        if self.carlight_pressed == 0:
            self.carlight_pressed = 1
        elif self.carlight_pressed == 1:
            self.carlight_pressed = 0

        self.carLight.setStyleSheet("background-color:" + str(color) + ";border-radius:5px;")

    # Open and close the interior light
    def carLight(self):
        if self.carlight_pressed == 1:
            self.setcarLight("white")
        else:
            self.setcarLight("lightblue")

    ############################### EXERCISE 10 ##############################
    # Unlock car
    def unlockCar(self):
        if self.carlight_pressed == 1:
            self.carlight_pressed = 0
        elif self.carlight_pressed == 0:
            self.carlight_pressed = 1
            self.setcarLight("lightblue")

        stop_event = threading.Event()
        t1 = threading.Thread(target=self.UnlockCarThread, args=(stop_event,))
        t1.daemon = True
        t1.start()

    def UnlockCarThread(self, stop_event):
        self.setWarningLights("orange", "orange", "orange", "orange")
        time.sleep(1)
        self.setWarningLights("white", "white", "white", "white")
        time.sleep(1)
        self.setWarningLights("orange", "orange", "orange", "orange")
        time.sleep(1)
        self.setWarningLights("white", "white", "white", "white")
        time.sleep(1)

        

    ############################### EXERCISE 11 ##############################
    # Lock the car
    def LockCar(self):
        
        if self.warning_pressed == 1:
            self.warning_pressed = 0
        
        if self.left_turn_pressed == 1:
            self.left_turn_pressed = 0
        
        if self.right_turn_pressed == 1:
            self.right_turn_pressed = 0

        stop_event = threading.Event()
        t1 = threading.Thread(target=self.LockCarThread, args=(stop_event,))
        t1.daemon = True
        t1.start()

    def LockCarThread(self, stop_event):
        self.setcarLight("white")
        self.setWarningLights("orange", "orange", "orange", "orange")
        time.sleep(1)
        self.setWarningLights("white", "white", "white", "white")


class MyWindow(QtGui.QMainWindow):
    def closeEvent(self, event):
        result = QtGui.QMessageBox.question(self,
                                            "Confirm Exit",
                                            "Are you sure you want to exit ?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        if result == QtGui.QMessageBox.Yes:
            event.accept()

        elif result == QtGui.QMessageBox.No:
            event.ignore()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    MainWindow = MyWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.center()
    sys.exit(app.exec_())
