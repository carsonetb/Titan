class Timer:
    def __init__(self, time, autostart, one_shot):
        self.init_time = time
        self.time_left = time
        self.running = autostart
        self.one_shot = one_shot

    def update(self, delta_time):
        if self.running:
            self.time_left -= delta_time
        
        if self.time_left < 0:
            if self.one_shot:
                self.running = False

            self.time_left = self.init_time
            
            return True

        return False
        
    def start(self):
        self.running = True
    
    def stop(self):
        self.running = False
        self.time_left = self.init_time

