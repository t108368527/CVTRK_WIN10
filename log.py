
class LOG():
    def __init__(self):
        self.level = ['E', 'W', 'D']

    def PY_LOG(self, level, message):
        if level ==  self.level[0]:         
            print("(error):  %s" % message)
        elif level == self.level[1]:       
            print("(warning):  %s" % message) 
        elif level == self.level[2]:       
            print("(debug): %s" % message)                                                                                          
                                         

    


