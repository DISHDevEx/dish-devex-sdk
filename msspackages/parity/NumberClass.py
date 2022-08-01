import math

class Number:
    def __init__(self,number):
        self.number = number
        
    def parity(self):
        if self.number % 2 == 0:
            return 'even'
        elif self.number % 2 == 1:
            return 'odd'
    