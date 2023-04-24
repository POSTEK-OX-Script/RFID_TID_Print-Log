"""
 RFID TID Print & Log: POSTEK OX Script Demos

 This is a simple demonstration of how OX Script can be used with RFID 
 applications. The TID is just one of the many data points that can be 
 retrieved and can then be easily written to databases, logged inside 
 the printer, used to fetch specific data from databases, or help encrypts 
 the data. 

 All debuglog() statements are printed to the printer's debug log.
    Not necessary for the script to run, but useful for debugging.

 Disclaimer:
    This software is provided "as is" and the author of the software is not liable for any damages or losses that may arise from the use of the software. Use at your own risk.
"""

from ox_script import *
import time as tt

#number of labels to be printed
num_label_to_print = 1 

#Retrieves how many labels to be printed
def inputnum(value):
    global num_label_to_print
    debuglog('The number of labels to be printed' + value)
    if value.isdigit():
        num_label_to_print = int(value)
    else:
        controller["Widget_1"].update("Print quantity input error!")

#Code related to label design 
def print_label(data):
    PTK_SetLabelHeight(height=1062,gapH=48)
    PTK_SetLabelWidth(width=1298)
    PTK_DrawText(x_coordinate=120,
            y_coordinate=590,
            fonts="4",
            font_size=1,
            data=data,
            text_style=NORMAL,
            rotation= 0,
            horizontal_multiplier= 1)
    PTK_DrawBar2D_QR(
        x_coordinate=350,
        y_coordinate=180,
        multiplier=11,
        data=data,
        encode_mode=4,
        correction_level=1,
        qr_version=0,
        masking=8,
        rotation=0,
    )
    PTK_PrintLabel(1, 1)

def run(value):
    debuglog(value)
    time = 0
    #used to keep track how many labels have been printed in this session
    #useful when nums > 1
    printed_copies = 0
    global num_label_to_print
    PTK_SetUnit(DOTS)
    if num_label_to_print < 1:
        return
    while 1:
        data = PTK_ReadRFID(0, 3, 0, 10)
        if data != -1:
            debuglog(data)
            controller["Widget_1"].update(data)
            print_label(data)
            printed_copies +=1
            controller["Widget_2"].update(printed_copies)
            num_label_to_print -= 1
            #If the user wanted to print more than 1 label at the same time
            while 1:
                tt.sleep(1)
                if num_label_to_print == 0:
                    return 0
                if GetPrinterStatus() == 100000:
                    data = PTK_ReadRFID(0, 3, 0, 10)
                    if data != -1:
                        debuglog('RFID Read Success')
                        debuglog(data)
                        controller["Widget_1"].update(data)
                        print_label(data)
                        printed_copies +=1
                        controller["Widget_2"].update(printed_copies)
                        num_label_to_print -= 1
                        debuglog("Labels to be printed:")
                        debuglog(num_label_to_print)
                    else:
                        debuglog('读取失败')
                        controller["Widget_2"].update("RFID Reading Failed:" + str(time+1))
                        time += 1
                        if time == 3:
                            return -1 
        else:
            controller["Widget_1"].update("RFID Reading failed:" + str(time+1))
            time += 1
            if time == 3:
                controller["Widget_1"].update("Please re-enter print quantity")
                return -1 
            
# The following code is used to initialize the UI on the printer
controller = UIInit(
    UIPage(
    		UIInput(Onpressed=inputnum, name="Print Quantities", value='1'),
    		UIInputbox(title="Printed Copies", value='0'),
    		UIInputbox(title="TID", value='0'),
    		UIButton(Onpressed=run, name="Start Printing"),
    ),
    # Setting require_execute_confirmation to False will allow the script 
    # to run without the need to press the execute button on the printer
    require_execute_confirmation=False,
)
#Since the script requires user input, no main loop is needed