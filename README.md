# nanopen-manipulator
Tool to precisely manipulate and automate NanoPen experiments

Run "python3 main.py"

**Requirements**:
- PySide6
- pyqtgraph
- numpy
- pyserial
- PyPylon
- cv2

# Guide
Upon running main.py, two windows will open up: "Nanopen Manipulator" and "Automation." For short, NPM and Autodia. NPM is a PyQtgraph-based XYZ manipulation GUI that plugs directly into any serial-based communication device, such as an Arduino. The "File" button is specifically for Autodia, and will be detailed below. "Serial" automatically searches through all open ports and will display, if recognized, each device name in a list. This allows for easy selection of an Arduino, or some other microcontroller. The serial commands are sent in a standardized string-format. For XYZ positions, it's "PX;Y;Z" with X, Y, and Z as integer positions, and P signialling a position command. The Arduino can process any string, and the program has various other button-based commands, such as "S" for stop, "H" for home, and so on. By default, "Home" is disabled to prevent accidental homing program activations, which can cause significant damage to the NanoPen if not careful. Finally, the "Units" button allows you to switch between stepper motor 'steps' and the actual estimated distance in micrometers.

Several buttons perform the following actions:
- Length/Width/Height: Sets software limits for XYZ boundaries to prevent moving past a specific region.
- Save Point: Opens a dialog for saving a particular position and assigning a name.

![image](https://github.com/user-attachments/assets/2acf6755-b5d7-4467-b786-c8631667c0f8)

- Step Size: Determines the number of steps, or approximate microns, the stepper motors will move. While in "Step Mode," the motors will step piecewise, one step at a time. While not in "Step Mode," the motors will move X steps * speed * 30 / s. This is calculated by applying speed as a float between 0 and 1, and 30 as the refresh rate of the program.
- Step Mode: As previously discussed, switches between 'stepping' and continuous movement.
- Free Mode: By default, the LWH limits are software locked, but when free mode is activated, these are ignored.
- Set Zero: Resets reference point to current position.
- Home: Automatically runs hard-coded homing program on the Arduino. This moves each motor as far as possible until a physical limit switch is activated, saves the distances, and adjust the software LWH limits accordingly.
- Origin: Moves to (0, 0, 0).

When successfully connected to the Arduino, the status indicator on the bottom will show "Connected to ####" and the current position of the motors will appear as "CX;Y;Z."

# Nanopen Manipulator
![image](https://github.com/user-attachments/assets/6ace0c1d-5a3b-4c8c-b546-75d3e87e606c)

The second window, "Automation," is for plugging into various instruments to conduct experiments with the NanoPen:
- Basler acA1300-200 μm camera
- Agilent 33220A function generator
- 2x Keithley DMM6500 multimeters
These can all be selected from the dropdown menus under the "Instruments" section. If no camera is connected, you can also load a prerecorded video under the "Camera" dropdown menu by selecting "Load Video."

Under the "Settings" section, there are two tabs: "Experiments" and "Video." "Experiments" allows you to set various hard-coded parameters defined within the "runExperiment" function in main.py, and in "switchExperiments" in auto.py. "Video" allows you to apply various filters, such as gaussian blur, adaptive thresholding, dilation, and color inversion. Amongst these is a "Frame Differencing" setting. When thresholding has been applied, you can enable frame differencing to identify all moving objects across a video in real-time. To track an object across time, hover over an identified object (red rectange) until it turns green, and click. The program will paint a green circle where the center of the object originated, a red circle at the current center, and draw a line between the two to better visualize motion. You can also use the scrollwheel to zoom into the center of the object for better viewing. The program will attempt to best maintain tracking, but at low FPS, under high noise, or low resolution, it may lose track. Currently, this function was designed to hook into an FPGA/Function Generator for PID control, but has yet to be fully implemented, and serves as a visual tool instead.

Under "Experiments," there is a "Save Directory" button to set your folder to save recordings to. The various buttons below the video act as one would expect, with a play, pause, screenshot (not-implemented yet), record, stop, and restart camera (or reset video) button. When the record button is pressed, the experiment will run, automatically applying voltages, changing polarities, and recording specified durations of video(s) to the save directory, with appropriate naming. The program also saves a .csv file with the timestamps and voltages measured from the multimeters. Currently, it does not save both the X and Y, but only whichever is applied at the moment. This is because all the experiments of interest to me apply voltages in the X and Y directions independently, and not at the same time, so I have no need for both. This can easily be changed by adjusting the "dataAcquisition" function in auto.py to save both X and Y voltages. A progress bar alongside a timer provides an estimated time to completion, but it is just an approximation, as it's difficult to take into account how long the motors take to move, the relay to switch polarities, waiting for the electrodes to dissipate charge, etc., so it's not a definitive judgment of completion, but a helpful tool nonetheless.

# Automation
![Screenshot 2025-04-28 001739](https://github.com/user-attachments/assets/35c56761-1943-4370-88b6-cde174e990f6)

