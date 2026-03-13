# -*- coding: utf-8 -*-
"""
Created on Mon Jun 30 17:18:16 2025

@author: kawdi
"""
import random as rd
import pygame as pg
import RDS
import numpy as np
import csv
from datetime import date
import GPIOpulse as GPIO

def gray(im):
    im = 255 * (im / im.max())
    w, h = im.shape
    ret = np.empty((w,h,3),dtype=np.uint8)
    ret[:,:,2] = ret[:,:,1] = ret[:,:,0] = im
    return ret

class Configuration:
    def __init__(self,user_id,clock,screen,spot_direction,camera,threshold,glasses):
        self.camera = camera
        self.user_id = user_id
        self.threshold = threshold
        self.glasses = glasses
        self.clock = clock
        self.subclock = 0
        self.screen = screen
        self.spot_direction = spot_direction
        self.activespot = spot_direction[0]
        self.spot_list = [0,1,0,2,0,3,0,4]
        self.point = 0
        self.fields = ['user_id','active_spot','time(ms)','Left_x_pos','Left_y_pos','Right_x_pos','Right_y_pos']
        self.data = []
    def track(self):
        l_location, r_location = self.camera.l_r_positions()
        if l_location is None:
            l_location = ('n/a','n/a') 
        if r_location is None:
               r_location = ('n/a','n/a')
        if any(map(len, l_location)) and any(map(len, r_location)) and (len(r_location) > 0 and len(l_location) > 0):
               self.data.append([self.user_id,self.activespot,str(self.clock),str(l_location[-2]),str(l_location[-1]),str(r_location[-2]),str(r_location[-1])])
        else:
               self.data.append([self.user_id,self.activespot,str(self.clock),'n/a','n/a','n/a','n/a'])
    def cycle(self):
        self.subclock += 1
        if self.subclock > 4000:
           self.point += 1
           self.subclock = 0
    def display_green(self):
        green_space = self.spot_list[self.point]
        self.activespot = self.spot_list[green_space]
        return green_space
    def file_record(self):
            today = date.today().strftime("%Y_%B_%d")
            filename = self.user_id + '_' + 'configuration' + '_' + today
            with open(filename, 'w') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(self.fields)
                csvwriter.writerows(self.data)        
    
    
class PsychoPhys:
    def __init__(self,user_id,clock,screen,camera,threshold,glasses):
        self.screen = screen
        self.camera = camera
        self.threshold = threshold
        self.glasses = glasses
        self.user_id = user_id
        self.clock = clock
        self.iteration = 0
        self.fields = ['user_id','iteration','time(ms)','Left_x_pos','Left_y_pos','Right_x_pos','Right_y_pos']
        self.data = []
        
    def track(self):
        if self.iteration <= 10:
           l_location, r_location = self.camera.l_r_positions()
        if l_location is None:
            l_location = ('n/a','n/a') 
        if r_location is None:
               r_location = ('n/a','n/a')
        if any(map(len, l_location)) and any(map(len, r_location)) and (len(r_location) > 0 and len(l_location) > 0):
               self.data.append([self.user_id,str(self.iteration),str(self.clock.get_time()),str(l_location[-2]),str(l_location[-1]),str(r_location[-2]),str(r_location[-1])])
        else:
               self.data.append([self.user_id,str(self.iteration),str(self.clock.get_time()),'n/a','n/a','n/a','n/a'])
    def load_rds(self,screen,size):
        mask = RDS.masks[rd.randint(0,3)]
        imgOn, imgOff = RDS.individuals_RDS(mask,1)
        imgOn, imgOff = gray(imgOn), gray(imgOff)
        imgOn, imgOff = pg.surfarray.make_surface(imgOn), pg.surfarray.make_surface(imgOff)
        
        pos_on = (int(3*size[0]/4)-296,180)
        pos_off = (int(size[0]/4)-216,180)
        return imgOn, pos_on, imgOff, pos_off
    def file_record(self):
            today = date.today().strftime("%Y_%B_%d")
            filename = self.userid + '_' + 'psychophys' + '_' + today
            with open(filename, 'w') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(self.fields)
                csvwriter.writerows(self.data)
                
class ElectroPhys:
    def __init__(self,user_id,clock,screen,camera,threshold,glasses,active):
        self.screen = screen
        self.size = pg.display.get_window_size()
        self.camera = camera
        self.threshold = threshold
        self.glasses = glasses
        self.user_id = user_id
        self.clock = 0
        self.active = active
        self.state = ''
        self.fields = ['user_id','active','time(ms)','Left_x_pos','Left_y_pos','Right_x_pos','Right_y_pos']
        self.data = []
    
    def track(self):
        l_location, r_location = self.camera.l_r_positions()
        if not any(map(len, l_location)):
            l_location = ('n/a','n/a') 
        if not any(map(len, r_location)):
               r_location = ('n/a','n/a')
        if any(map(len, l_location)) and any(map(len, r_location)):
                self.data.append([self.user_id,self.state,str(self.clock.get_time()),str(l_location[-2]),str(l_location[-1]),str(r_location[-2]),str(r_location[-1])])
        else:
                self.data.append([self.user_id,self.state,str(self.clock.get_time()),'n/a','n/a','n/a','n/a'])
                
    def form_rds(self,shift):
        mask = RDS.masks[1]
        imgOn, imgOff = RDS.individuals_RDS(mask,shift)
        imgOn, imgOff = gray(imgOn), gray(imgOff)
        imgOn, imgOff = pg.surfarray.make_surface(imgOn), pg.surfarray.make_surface(imgOff)
        return imgOn, imgOff
    def load_rds(self,screen,size,imgOn,imgOff):
        pos_on = (int(3*size[0]/4)-296,180)
        pos_off = (int(size[0]/4)-216,180)
        if self.active:
            screen.blit(imgOff,pos_off)
            screen.blit(imgOn,pos_on)
        else:
            screen.blit(imgOff,pos_off)
            screen.blit(imgOff,pos_on)    
    def update(self):
        self.active = not self.active
        swap = True
        clock_call = self.clock
        return swap, clock_call
    def swap(self,clock_call):
        self.state='Transitioning'
        active_time = self.clock - clock_call
        if (active_time % 720) == 0:
            ElectroPhys.pulse(self)
            return False
        else:
            swapping_time = (self.clock - clock_call)/720 if self.active else (1-(self.clock - clock_call)/720)
            imgOn, imgOff = ElectroPhys.form_rds(self,swapping_time)
            ElectroPhys.load_rds(self,self.screen,self.size,imgOn,imgOff)
            self.state = 'On' if self.active else 'Off'
            return True
            
    def pulse(self):
        GPIO.gpio_pulse(self.active)
        pass
    def file_record(self):
            today = date.today().strftime("%Y_%B_%d")
            filename = self.userid + '_' + 'electrophys' + '_' + today
            with open(filename, 'w') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(self.fields)
                csvwriter.writerows(self.data)