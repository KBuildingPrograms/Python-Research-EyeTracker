# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 15:39:08 2025

@author: kawdi
"""

import pygame as pg
import cv2
import sys
import os
import button as bt
import RDS
import TryCam as tc
import Experiment as exp
import random
import string



def resources_path(relative_path): #path guide for Pyinstaller
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path,relative_path)

pg.init()
pg.font.init()
flags = pg.FULLSCREEN 
resolution = (1920,1080)
bpp = 16
screen = pg.display.set_mode(resolution, flags, bpp)
font = 'arial'
fontsize = 24
default_font = pg.font.SysFont(font, fontsize)
sub_fontsize = 16
sub_font = pg.font.SysFont(font, sub_fontsize)
clock = pg.time.Clock()
timer = clock.tick(170) #Sets the rate to 1 refresh every 5.8ms which isn't nyquist to microsacchades but it should be able to detect rapid eye movement
size = pg.display.get_window_size()

#Camera settings
camera = cv2.VideoCapture(0)
glasses = False #altered based on whether or not the user is wearing glasses
threshold = 40 #Basic useful starting threshold
UserID = ''

#Instruction Section
def about():
    about_text = "-Updated screensize \n -Updated program speed and size \n -Fixed eyeline guide placement \n -Testing opens the webcamera and allows for altering the threshold and presence of glasses to optimize eye detection \n -Pyschophysiological portion altered to be a tap when depth detected version \n -Electrophysiological experiment collapses and forms every 5 seconds over a 720ms interval, pulse is still being worked on \n -The testing mode is still on if you'd like to close the application during an experiment \n -Karyn (7/23/25)"
    back_button = bt.Button(image=None, pos=(size[0]-30,size[1]-20), text_input="Back", font=default_font,
                            base_color='blue', hovering_color='green')
    while True:
        about_mouse_pos = pg.mouse.get_pos()
        screen.fill('azure2')
        bt.paragraph_blit(screen, about_text, (20,80), default_font, 500, 800)
        back_button.changeColor(about_mouse_pos)
        back_button.update(screen)
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                break
            if event.type == pg.MOUSEBUTTONDOWN:
                if back_button.checkForInput(about_mouse_pos):
                    menu()
                    break

def instruct():
    global size
    pg.display.set_caption("Instruction")
    Top_text = "Instructions"
    tt = bt.Text(Top_text,(10,10),45)
    ins_text = "This is where the instructions on how to view a random dot stereogram (RDS) and specific set up for the methodolgy (camera set up, head distance from screen, etc.)"
    ins_text2 = "Testing is where you can test your camera to make sure it's connected, and where you can adjust your settings. Both tests will use these settings, so make sure it's consistently detecting your eye. After which you will configure the system so the movement of your eyes is correlated to specific spots on screen."
    ins_text3 = "The Psychophysiological form of experiment uses your input. As you view an RDS, you will hold the space key. Once you visualize depth, you will release the key. The next stereogram will appear once you press and hold the key again"
    ins_text4 = "The Electrophysiological experiment will require that your connected to the BIOPAC EEG first. The RDS will form and collapse at a set rhythm."
    center_im = pg.image.load(resources_path("Photos/Instructions.png")).convert()
    center_im = pg.transform.scale(center_im,(int(size[0]*3/8),int(size[0]*3/8)))
    while True:
        #screen set up
        screen.fill('gray')
        instr_mouse_pos = pg.mouse.get_pos()
        tt.draw(screen)
        
        #button set up
        back_button = bt.Button(image=None, pos=(size[0]-30,size[1]-20), text_input="Back", font=default_font,
                                base_color='blue', hovering_color='green')
        back_button.changeColor(instr_mouse_pos)
        back_button.update(screen)
        
        next_button = bt.Button(image=None, pos=(size[0]-100,size[1]-20),text_input="Next",font=default_font, base_color='blue',
                                hovering_color='green')
        next_button.changeColor(instr_mouse_pos)
        next_button.update(screen)
        
        #paragraph set up
        bt.paragraph_blit(screen, ins_text, (30,50), default_font,270, 150)
        bt.paragraph_blit(screen,ins_text2,(30,250),default_font,270,150)
        bt.paragraph_blit(screen,ins_text3,(290,50),default_font,530,150) #there's an issue I need to fix where the width is actually width-position
        bt.paragraph_blit(screen,ins_text4,(290,350),default_font,530,150) #yep, that's the problem
        
        #instruction set up
        screen.blit(center_im,(700,250))
          
        guide_text = "Make sure to align your eye level with the center of the screen. You can move the window around the screen to better position it with your vision. Additionally, sit approximately 24 inches from the screen." 
        bt.paragraph_blit(screen,guide_text,(700,20),default_font,1000,150)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                break
            if event.type == pg.MOUSEBUTTONDOWN:
                if back_button.checkForInput(instr_mouse_pos):
                    menu()
                    break
                if next_button.checkForInput(instr_mouse_pos):
                    practice()
                    break
        pg.display.update()
        
def practice():
    pg.display.set_caption("RDS Test")
    global size
    prac_text = "Below you will see an example of a random dot stereogram. To visualize it you can diverge your eyes such that you see 3 of the red squares at the top of the screen, then holding said position as you guide your eyes to the RDS."
    prac_text2 = "To do so, you can move closer to the screen such that your see 3 of the guidance squares above. When you hold your eyes in that position, you should be able to visualize the RDS. With a small bit of practice, you can automatically adjust your eyes to view it."
    guide_rect1 = pg.Rect(480,120,15,15)
    guide_rect2 = pg.Rect(1360,120,15,15) #still need to fix these
    try:
        #generates rds based on the sphere mask
        rds_on, rds_off = RDS.individuals_RDS("Photos/sphere_mask.png",2)
        rds_on, rds_off = RDS.gray(rds_on), RDS.gray(rds_off)
        rds_on, rds_off = pg.surfarray.make_surface(rds_on), pg.surfarray.make_surface(rds_off)
    except Exception as e:
        print(e)
    while True:
        size = pg.display.get_window_size()
   
        prac_mouse_pos = pg.mouse.get_pos()
        screen.fill('azure3')
        bt.paragraph_blit(screen,prac_text,(30,50),default_font,1200,150)
        bt.paragraph_blit(screen,prac_text2,(30,1230),default_font,1200,150)
        
        back_button = bt.Button(image=None, pos=(size[0]-30,size[1]-20), text_input="Back", font=default_font,
                                base_color='blue', hovering_color='green')
        back_button.changeColor(prac_mouse_pos)
        back_button.update(screen)
        
        try:
            pg.draw.rect(screen,'red',guide_rect1)
            pg.draw.rect(screen,'red',guide_rect2)
            screen.blit(rds_off,(int(size[0]/4)-216,180))
            screen.blit(rds_on,(int(3*size[0]/4)-296,180))
        except Exception as e:
            print(e)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                break
            if event.type == pg.MOUSEBUTTONDOWN:
                if back_button.checkForInput(prac_mouse_pos):
                    instruct()
                    break
        pg.display.update()

#Testing and Configuration
def test():
    global glasses
    global threshold
    pg.display.set_caption("Test & Practice")
    CameraOn = False
    visual = tc.MainCamera((300,100),camera,threshold,glasses)
    tick = 0
    total = 0
    percentage = 0
    close_cam = bt.Button(image=None, pos=(50,650),text_input="Close Camera", font=default_font, base_color='blue',hovering_color='green')
    inc_thr = bt.Button(image=None, pos=(600,600),text_input='+', font=default_font, base_color='black', hovering_color='blue')
    dec_thr = bt.Button(image=None, pos=(600,650),text_input='-',font=default_font, base_color='black',hovering_color='blue')
    threshold_text = bt.Text(str(threshold),(600,625),fontsize=15)
    glass_button = bt.Button(image=None, pos=(600,675), text_input='Wearing Glasses:', font=default_font, base_color='blue', hovering_color='black')
    back_button = bt.Button(image=None, pos=(1250,700), text_input="Back", font=default_font,
                            base_color='blue', hovering_color='green')
    configure_button = bt.Button(image=None, pos=(1160,700),text_input = "Configure",font=default_font,base_color='blue',hovering_color='green')
    while True:
        test_mouse_pos = pg.mouse.get_pos()
        test_text = "Open your camera and alter the threshold till you consistently see 100% detection, and the glasses flag based on any eyewear. Sit in a space with plenty of even lighting."
        test_cam = bt.Button(image=None, pos=(50,600),text_input="Test Camera", font=default_font,
                         base_color='blue', hovering_color='green')
        if not CameraOn:
            screen.fill('gray')
            test_cam.changeColor(test_mouse_pos)
            test_cam.update(screen)
        
        
        if CameraOn:
            screen.fill('gray')
            close_cam.changeColor(test_mouse_pos)
            close_cam.update(screen)
            inc_thr.changeColor(test_mouse_pos)
            inc_thr.update(screen)
            dec_thr.changeColor(test_mouse_pos)
            dec_thr.update(screen)
            threshold_text.draw(screen)
            glass_button.changeColor(test_mouse_pos)
            glass_button.update(screen)
            if glasses:
                glasses_text = bt.Text('True',(690,667),fontsize=25)
                glasses_text.draw(screen)
        
        
        back_button.changeColor(test_mouse_pos)
        back_button.update(screen)
        configure_button.changeColor(test_mouse_pos)
        configure_button.update(screen)
        
        bt.paragraph_blit(screen, test_text, (30,50), default_font, 800, 100)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if camera.isOpened():
                    cv2.destroyAllWindows()
                pg.quit()
                sys.exit()
                break
            if event.type == pg.MOUSEBUTTONDOWN:
                if test_cam.checkForInput(test_mouse_pos) and not CameraOn:
                    CameraOn = True
                if close_cam.checkForInput(test_mouse_pos) and CameraOn:
                    CameraOn = False
                    screen.fill('gray') #I DID IT
                if inc_thr.checkForInput(test_mouse_pos) and threshold < 255:
                    threshold += 1
                if dec_thr.checkForInput(test_mouse_pos) and threshold > 0:
                    threshold -= 1
                if glass_button.checkForInput(test_mouse_pos):
                    glasses = not glasses
                if back_button.checkForInput(test_mouse_pos):
                    if camera.isOpened():
                        cv2.destroyAllWindows()
                    menu()
                if configure_button.checkForInput(test_mouse_pos):
                    if camera.isOpened():
                        cv2.destroyAllWindows()
                    config_preamb()
                    break
        if CameraOn:
            try:
                visual.render()
                total += visual.detection_freq()
                tick += 1
                visual.draw(screen)
            except:
                pass
            if tick >= 99:
                percentage = int(total/tick)*100
                tick = 0
                total = 0
            percent_text = bt.Text(str(percentage)+"%",(650,625),fontsize=15)
            percent_text.draw(screen)
        pg.display.update()




#Experiment Pre-Section
def user_id_read():
    f = open("UserIDs.txt")
    if not f.closed:
        IDlist = f.read().splitlines()
        return IDlist
    else:
        return []

def user_id_gen():
    length = 8
    new_user = ''.join(random.choices(string.ascii_letters+string.digits,k=length))
    f = open("UserIDs.txt",'r+')
    if not f.closed:
        IDlist = f.readlines()
        while new_user +'\n' in IDlist:
            new_user = ''.join(random.choices(string.ascii_letters+string.digits,k=length))
            if new_user not in IDlist:
                break
        f.writelines([new_user+'\n'])
    return new_user

def config_preamb():
    global UserID
    size = pg.display.get_window_size()
    config_text = "The following configuration section will require you to look at alternating green spots across the page. The configuration begins with the middle green spot and switches between it and the surrounding 4.\nOnce the configuration ends you will return to the menu to continue with the next experiment. Below you can generate an ID to be associated with the data or write an ID you've previously generated. Keep your head still during configuration and further experiments."
    ID_pretext = bt.Text("Current ID:",(30,325),20)
    ID_pretext2 = bt.Text("Or Enter ID:",(30,350),20)
    gen_button = bt.Button(image=None,pos=(70,300),text_input="Generate ID",font=default_font,base_color='blue',hovering_color='green')
    next_button = bt.Button(image=None,pos=(size[0]-50,size[1]-30),text_input="Configure",font=default_font,base_color='blue',hovering_color='green')
    ID_m = ''
    ID_manual_bool = False
    ID_manual_entry = bt.TextEntry(text=ID_m,pos=(110,350),font=default_font,base_color='azure4',active_color='azure',active=ID_manual_bool)
    #IDList = user_id_read()
    while True:
        ID_manual_bool = False
        ID_manual_entry = bt.TextEntry(text=ID_m,pos=(110,350),font=default_font,base_color='azure4',active_color='azure',active=ID_manual_bool)
        ID_text = bt.Text(UserID,(105,325),20)
        cpreamb_mouse_pos = pg.mouse.get_pos()
        screen.fill('azure3')
        bt.paragraph_blit(screen, config_text, (30,30), default_font, 400, 200)
        gen_button.update(screen)
        gen_button.changeColor(cpreamb_mouse_pos)
        next_button.update(screen)
        next_button.changeColor(cpreamb_mouse_pos)
        ID_pretext.draw(screen)
        ID_text.draw(screen)
        ID_pretext2.draw(screen)
        ID_manual_entry.update(screen)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                break
            if event.type == pg.MOUSEBUTTONDOWN:
                if gen_button.checkForInput(cpreamb_mouse_pos):
                    UserID = user_id_gen()
                    print(UserID)
                if next_button.checkForInput(cpreamb_mouse_pos):
                    try:
                        configuration()
                    except Exception as e:
                        print(e)
                if ID_manual_entry.checkForInput(cpreamb_mouse_pos):
                    ID_manual_bool = True
                else:
                    ID_manual_bool = False
            if event.type == pg.KEYDOWN:
                ID_m = ID_manual_entry.get_text(event, ID_m)
        pg.display.update()

def psyphy_preamb():
    global screen
    size = pg.display.get_window_size()
    while True:
        screen.fill('azure3')
        intro_text = "Hello, welcome to the psychophysical data recollection"
        pt_text = bt.Text(intro_text, (20,20), 45)
        pt_text.draw(screen)
        instr_text = "Before you continue, look towards the red dots in the center of the page. This is where you will look for each Random Dot Stereogram (RDS). Hold your fingers over the space key. You will press the space key to activate the RDS, and press it again once you perceive depth. You also won't be able to close the application until the experiment is complete."
        bt.paragraph_blit(screen, instr_text, (20,100), default_font, 700, 200)
        state_text = bt.Text("Tap space to start",(593,375),15)
        state_text.draw(screen)
        pg.draw.circle(screen, 'red', (int(size[0]/2)+271,int(size[1]/2)), 5)
        pg.draw.circle(screen, 'red', (int(size[0]/2)-271,int(size[1]/2)), 5)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit
                break
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    psychophys()
        pg.display.update()
        
def elect_preamb():
    global screen
    size = pg.display.get_window_size()
    intro_text = "Hello! Welcome to the electrophysical data recollection, which is still under construction"
    et_text = bt.Text(intro_text,(20,20), 45)
    instr_text = "Before you begin, make sure you're wearing the biopac electrodes, and the biopac is reading your brain activity. This section of the demo is not fully operable yet for the eeg but should still function."
    instr_text2 = "Stare at the center of the screen where the red dots are. The RDS will form and colapse at a set interval. You won't need to manually input anything."
    while True:
       screen.fill('azure2')
       et_text.draw(screen)
       bt.paragraph_blit(screen, instr_text, (20,80), default_font, 300, 200)
       bt.paragraph_blit(screen,instr_text2,(20,350),default_font,300,200)
       pg.draw.circle(screen, 'red', (int(size[0]/2)+271,int(size[1]/2)), 5)
       pg.draw.circle(screen, 'red', (int(size[0]/2)-271,int(size[1]/2)), 5)
       state_text = bt.Text("Tap space to start",(593,375),15)
       state_text.draw(screen)
       for event in pg.event.get():
           if event.type == pg.QUIT:
               pg.quit()
               sys.exit
               break
           if event.type == pg.KEYDOWN:
               if event.key == pg.K_SPACE:
                   electrophys()
                   break
       pg.display.update()

#Experiments
def configuration():
    size = pg.display.get_window_size()
    current = pg.time.get_ticks()
    active_time = 0
    pg.display.set_caption('Configuration')
    eye_tracker = tc.MainCamera((0,0), camera, threshold, glasses)
    green_spot = [(int(size[0]/2),int(size[1]/2)),(int(size[0]/2),int(size[1])-10),(int(size[0]/2),10),(10,int(size[1]/2)),(int(size[0])-10,int(size[1]/2))]
    spot_direction=['middle','down','up','left','right']
    tracker = exp.Configuration(UserID, active_time, screen, spot_direction, eye_tracker, threshold, glasses)
    #midle, down, up, left, right
    while True:
        screen.fill('azure3')
        pg.draw.circle(screen, 'red', green_spot[0],10), pg.draw.circle(screen, 'red', green_spot[1],10), pg.draw.circle(screen, 'red', green_spot[2],10), pg.draw.circle(screen, 'red', green_spot[3],10), pg.draw.circle(screen, 'red', green_spot[4],10)
        active_time = pg.time.get_ticks() - current
        pg.draw.circle(screen, 'green', green_spot[tracker.display_green()],10)
        tracker.cycle() 
        if tracker.point == 7:
            tracker.file_record()
            menu()
            break
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        pg.display.update()

def psychophys(): 
    global camera
    size = pg.display.get_window_size()
    pg.display.set_caption("PyschoPhysical Experiment")
    active = False
    testing = False
    eye_tracker = tc.MainCamera((0,0), camera, threshold, glasses)
    tracker = exp.PsychoPhys(UserID, clock, screen, eye_tracker, threshold, glasses)
    imgOn, posOn, imgOff, posOff = None,None,None,None
    guide_rect1 = pg.Rect(374,87,15,15)
    guide_rect2 = pg.Rect(906,87,15,15)
    while True:
        screen.fill('azure3')
        pg.draw.rect(screen,'red',guide_rect1)
        pg.draw.rect(screen,'red',guide_rect2)
        for event in pg.event.get():
            if event.type == pg.QUIT and (active==False or testing==True):
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                active = not active
                if active: tracker.iteration += 1
                imgOn,posOn,imgOff,posOff = tracker.load_rds(screen, size)
        if active:
            try:
                tracker.track()
                screen.blit(imgOn,posOn)
                screen.blit(imgOff,posOff)
            except Exception as e:
                print(e)
        track = "RDS: " + str(tracker.iteration) + "/10" 
        track_text = bt.Text(track,(20,20),25)
        track_text.draw(screen)
        if tracker.iteration == 10:
            tracker.file_record()
            menu()
        pg.display.update()
        
def electrophys():
    global camera
    current = pg.time.get_ticks()
    clock_ms = 0
    size = pg.display.get_window_size()
    pg.display.set_caption("ElectroPhysical Experiment")
    active = True
    testing = True
    swap = False
    eye_tracker = tc.MainCamera((0,0), camera, threshold, glasses)
    tracker = exp.ElectroPhys(UserID, clock_ms, screen, eye_tracker, threshold, glasses, active)
    imgOn, imgOff = tracker.form_rds(0)
    guide_rect1 = pg.Rect(374,87,15,15)
    guide_rect2 = pg.Rect(906,87,15,15)
    while True:
        screen.fill('azure3')
        pg.draw.rect(screen,'red',guide_rect1)
        pg.draw.rect(screen,'red',guide_rect2)
        tracker.load_rds(screen,size,imgOn,imgOff)
        clock_ms = pg.time.get_ticks()
        tracker.clock = clock_ms - current
        tracker.track()
        if tracker.clock % 5000 == 0:
            swap, clock_call = tracker.update()
        if swap:
            swap = tracker.swap(clock_call)
            print('swapping')
        if tracker.clock >= 30000: #setting the time limit to 30000 arbitrarily, translates to 30 seconds
            tracker.file_record()
            menu()
        for event in pg.event.get():
            if event.type == pg.QUIT and testing:
                pg.quit()
                sys.exit
                break
        pg.display.update()

def menu():
    pg.display.set_caption("2025 RDS and Eyetracking")
    size = pg.display.get_window_size()
    screen_text = bt.Text("2025 RDS and Eyetracking Experiment", (20,20), 45)
    instr_button = bt.Button(image=None, pos=(70,150), text_input="Instructions",
                          font=default_font, base_color='blue',hovering_color='green')
    test_button = bt.Button(image=None, pos=(50,180), text_input="Testing", font=default_font, base_color='blue',hovering_color='green')
    psyphy_button = bt.Button(image=None, pos=(130,240), text_input="Psychophysical Experiment", font=default_font, base_color='mediumpurple3',hovering_color='red')
    elecphy_button = bt.Button(image=None, pos=(130,270), text_input="Electrophysical Experiment", font=default_font, base_color='mediumpurple3', hovering_color='red')
    about_button = bt.Button(image=None, pos=(size[0]-90,size[1]-20), text_input="Version 1.50-About",font=default_font,base_color='blue',hovering_color='green')
    while True:
        menu_mouse_pos = pg.mouse.get_pos()
        screen.fill('white')
        screen_text.draw(screen)
        
        
        instr_button.changeColor(menu_mouse_pos)
        instr_button.update(screen)
        
        test_button.changeColor(menu_mouse_pos)
        test_button.update(screen)
        
    
        psyphy_button.changeColor(menu_mouse_pos)
        psyphy_button.update(screen)
        
        elecphy_button.changeColor(menu_mouse_pos)
        elecphy_button.update(screen)
        
        about_button.changeColor(menu_mouse_pos)
        about_button.update(screen)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                break
            if event.type == pg.MOUSEBUTTONDOWN:
                if instr_button.checkForInput(menu_mouse_pos):
                    instruct()
                    break
                if test_button.checkForInput(menu_mouse_pos):
                    test()
                    break
                if psyphy_button.checkForInput(menu_mouse_pos):
                    psyphy_preamb()
                    break
                if elecphy_button.checkForInput(menu_mouse_pos):
                    elect_preamb()
                    break
                if about_button.checkForInput(menu_mouse_pos):
                    about()
                    break
        pg.display.update()
        

menu()

