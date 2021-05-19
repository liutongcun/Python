#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  8 15:05:49 2021

@author: liutongcun
"""


class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self.odometer_reading = 0
        
    def get_descriptive_name(self):
        long_name = str(self.year) + ' ' + self.make + ' ' + self.model
        return long_name.title()
        
    def read_odometer(self):
        print('This car has ' + str(self.odometer_reading) + ' miles.')
        
    def update_odometer(self, mileage):
        if mileage >= self.odometer_reading:
            self.odometer_reading = mileage
        else:
            print("You can't roll back an odometer!")
            
    def increment_odometer(self, miles):
        self.odometer_reading += miles
        
class ElectricCar(Car):
    def __init__(self, make, model, year):
        # 初始化父类的属性：
        super().__init__(make, model, year) 
        # 子类独有的属性：
        self.battery_size = 70
        
    # 如果父类的方法不适用于子类，可在子类中重写父类的方法，会自动覆盖父类对应的方法。
    def get_descriptive_name(self):
        # 调用父类的同名方法：
        long_name = super().get_descriptive_name()
        return long_name + ' with ' + str(self.battery_size) + '-kwh Battery'
    
def get_name(n):
    print('你好,'+n)
    
    
if __name__=='__main__':       

    my_beetle = ElectricCar('volkswagen', 'beetle', 2016) 
    
    print(my_beetle.get_descriptive_name())
    my_beetle.read_odometer()
    my_beetle.increment_odometer(10)
    my_beetle.read_odometer()


