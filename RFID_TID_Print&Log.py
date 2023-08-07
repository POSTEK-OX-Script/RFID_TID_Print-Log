"""
 RFID TID Print & Log: POSTEK OX Script Demos

 This is a simple demonstration of how OX Script can be used with RFID 
 applications. The TID is just one of the many data points that can be 
 retrieved and can then be easily written to databases, logged inside 
 the printer, used to fetch specific data from databases, or help encrypts 
 the data. 

 Disclaimer:
    This software is provided "as is" and the author of the software is not liable for any damages or losses that may arise from the use of the software. Use at your own risk.
"""

from ox_script import *  # Importing the ox_script module

TID_controller = None  # Initializing the controller to None

def one_cycle():  # This function will execute everytime the button is pressed
    global TID_controller  # Accessing the global variable TID_controller
    data = PTK_ReadRFID(TID)  # Reading RFID 
    if data != -1:  
        data = data [0:20]  # Truncating the data to 20 characters
        PTK_SetLabelHeight(height=32.6)  # Setting the label height
        PTK_DrawBar2D_QR(
                            # Drawing a QR code
                            x_coordinate=25,
                            y_coordinate=10,
                            multiplier=6,
                            data=data,
                            )
        PTK_PrintLabel(1)  # Printing the label
        TID_controller.update(data)  # Updating the printer UI with the data

# If the script is being run as the main program
if __name__ == "__main__":  
    PTK_UIInit(
        PTK_UIPage(
            TID_controller := PTK_UITextBox(title="Tag TID:", value="--"),  # Creating a text box for the TID and assigns the controller
            PTK_UIButton(title="Start Reading", Onpressed=one_cycle),  # Creating a button to start reading RFID data
        ),
    )
