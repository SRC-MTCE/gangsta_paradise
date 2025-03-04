from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service

import time
import win32com.client
from win32gui import GetWindowText, GetForegroundWindow
import pythoncom
import os
from pynput.keyboard import Key, Listener, Controller
import pywinauto
import winsound
import pyautogui

import xml.etree.ElementTree as ET
import sys
import ctypes
import time 



alt_pressed = False
header = "Ganstga Paradise"

itx_password = os.environ.get("itx_pwd")

exe_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
xml_file = exe_dir + '/__config__.xml'
tree = ET.parse(xml_file)
root = tree.getroot()

control_point = root.find('active_control_point').text
print(f"Active Control Point: {control_point}")

keyboardd = Controller()




def click_at():
    # Move the mouse to the specified coordinates
    ctypes.windll.user32.SetCursorPos(70, 1050)
    
    # Mouse left down
    ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
    time.sleep(0.01)  # Small delay to simulate a real click
    
    # Mouse left up
    ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)
    time.sleep(0.01)

    # Move the mouse to the specified coordinates
    ctypes.windll.user32.SetCursorPos(2000, 1000)
    
    # Mouse left down
    ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
    time.sleep(0.01)  # Small delay to simulate a real click
    
    # Mouse left up
    ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)
    time.sleep(0.01)




def press_ctrl_shift_f2():
    time.sleep(0.05)
    keyboardd.press(Key.ctrl)
    keyboardd.press(Key.shift)
    keyboardd.press(Key.f2)
    time.sleep(0.05)
    keyboardd.release(Key.ctrl)
    keyboardd.release(Key.shift)
    keyboardd.release(Key.f2)

    
def log(data_to_write):
    if not os.path.isdir(".\\gangsta_log"):
        os.makedirs(".\\gangsta_log")
        
    filename = '.\\gangsta_log\\' + str(datetime.now().strftime('%Y-%m-%d')) + '-gangsta_paradise.log'
    with open(filename, 'a') as logfile:
        if os.path.getsize(filename) == 0:  # Check if the file is empty
            logfile.write(header)

        logfile.write(str(datetime.now().strftime('%H:%M:%S.%f')[:-3]) + ': ' + data_to_write + '\n')

def terminate_chromedriver():
    for proc in psutil.process_iter(['pid', 'name']):
        if 'chromedriver.exe' in proc.info['name']:
            log(f"Terminating chromedriver.exe with PID {proc.info['pid']}")
            proc.terminate()

def init_chrome_drivers(control_point):
    log(f"(init_chrome_driver)Opening Driver for Control Point {control_point}")
    try:
        #driver = webdriver.Chrome()
        chromedriver_path =  exe_dir + '/chromedriver_win64/chromedriver.exe' 
        print(chromedriver_path)
        # Initialize the Service with the chromedriver path
        service = Service(chromedriver_path)
        options = webdriver.ChromeOptions()
        options.add_argument(f"google-chrome --app=http://fs-gvplatform.pres.cbcrc.ca/fstvmain/channel-ganging-webui/permission/{control_point}")
        driver = webdriver.Chrome(service=service, options=options)
        pythoncom.CoInitialize() 
        driver.get(f'http://fs-gvplatform.pres.cbcrc.ca/fstvmain/channel-ganging-webui/permission/{control_point}')
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//*[@id="Username"]').send_keys("mtlitxadmin")
        driver.find_element(By.XPATH, '//*[@id="Password"]').send_keys(itx_password)
        shell = win32com.client.Dispatch("WScript.Shell")
        time.sleep(0.1)
        shell.Sendkeys("{ENTER}")
        time.sleep(1)
        driver.refresh()
        time.sleep(0.5)
        driver.maximize_window()
        log(f"(init_chrome_driver)Success! Driver oppenned for Control Point {control_point}")

    except Exception as driver_error:
        error_message = str(driver_error)
        print(error_message)
        log(error_message)
        
    return driver

def click_button(driver):
    try:  
        button = driver.find_elements(By.XPATH, f'//*[@id="gvApp"]/div[2]/div/div[1]/div[5]/button[2]')[0]
        button.click()
        log("Taking Next")
        print("Taking Next")
        
    except Exception as button_error:
        error_message = str(button_error)
        print(error_message)
        log(error_message)
        log("Most likely there is now Take Next") 

def handle_key_event(key):
    global driver, alt_pressed, function_key

    try:
        pute = key.char
        if pute == 'z':
            alt_pressed = True
            print("ALT pressed")
            
    except AttributeError:
        # Handle special keys
        if key in [Key.f13, Key.f14, Key.f15]:
            print(f"{key} pressed")
        
    if key in [Key.f13, Key.f14, Key.f15]:
        function_key = key
        if function_key == Key.f13 and alt_pressed:
            log("User clicked on ITX window button")
            try:
                app = pywinauto.Application().connect(title="iTX Desktop")
                window = app.window(title="iTX Desktop")
                window.minimize()
                window.restore()
                window.set_focus()

            except Exception as iTXd_error:
                error_message = str(iTXd_error)
                print("iTx Desktop page resore error! iTX desktop is most likely closed.")
                log(error_message)

        elif function_key == Key.f14 and alt_pressed:
            log("User clicked on Web Page Button")
            try:
                page_title = driver.title
                log("Page exists")
                
            except:
                page_title = None
                log("Page doesn't exist")
                pass

            if page_title:
                log("Putting GANG page in front")
                driver.minimize_window()
                driver.switch_to.window(driver.current_window_handle)
                driver.maximize_window()
                print("Maximizing window")
                
            else:
                log("Page down, restarting driver")
                try:
                    driver.quit()
                    log("Driver exited")
                    
                except:
                    pass
                
                driver = init_chrome_drivers(control_point)
                alt_pressed = False

        elif function_key == Key.f15 and alt_pressed:
            window = GetWindowText(GetForegroundWindow())
            if window == "iTX Desktop":
                print("Taking Next on iTX Desktop")
                log("Taking Next on iTX Desktop")
                #shell.Sendkeys("{CTRL}{SHIFT}{F2}")
                #press_ctrl_shift_f2()
                click_at()


            elif window == "Web UI":                
                try:
                    page_title = driver.title
                    log("Page exists")
                    
                except:
                    page_title = None
                    log("Page doesn't exist")
                    pass

                if page_title:
                    click_button(driver)
                        
                else:
                    log("Page down, restarting driver")
                    try:
                        driver.quit()
                        log("Driver exited")
                        
                    except:
                        pass

                    driver = init_chrome_drivers(control_point)
                    alt_pressed = False

            else:
                print("Windows sound notification")
                log("Nor iTX Desktop or iTX web driver are focused on! Issuing sound notification to user!")
                winsound.MessageBeep() 

def on_release(key):
    global alt_pressed, function_key
    

    try:
        pute = key.char
        if pute == 'z':
            alt_pressed = False
            print("ALT released")
    except AttributeError:
        # Handle special keys
        if key in [Key.f13, Key.f14, Key.f15]:
            print(f"{key} released")



    


# Initialize Chrome driver
driver = init_chrome_drivers(control_point)

# Register key press event handler
with Listener(on_press=handle_key_event, on_release=on_release) as listener:
    listener.join()

