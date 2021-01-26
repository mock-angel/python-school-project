import time

class JimData():
    def __init__(self, t_temp, t_heartrate, t_sweating, t_time = -1):
        self.k = t_temp       # K
        self.bpm = t_heartrate # BPM
        self.spm = t_sweating  # Gallons per day
        self.t = t_time       # Time

def JimMain(self):
    
    time.sleep(2)
    obj = JimData(30, 35,6, 9)
    self.insert_data(obj)
    
    time.sleep(2)
    obj = JimData(44, 38,6, 11)
    self.insert_data(obj)
    
    time.sleep(2)
    obj = JimData(56, 40,6, 13)
    self.insert_data(obj)
    
    time.sleep(2)
    obj = JimData(43, 38,6, 15)
    self.insert_data(obj)
    
    time.sleep(2)
    obj = JimData(31, 45,6, 17)
    self.insert_data(obj)
    
    time.sleep(2)
    obj = JimData(31, 45,6, 19)
    self.insert_data(obj)
    
    
    time.sleep(2)
    obj = JimData(31, 45,6, 20)
    self.insert_data(obj)
    
    time.sleep(2)
    obj = JimData(31, 45,6, 21)
    self.insert_data(obj)
    
    #self.save()
