# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 16:42:55 2025

@author: kawdi
"""
import pygame as pg
from pygame.locals import *
#thank you baraltech from youtube
#the most straightforward pygame tutorial to date

class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        
    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
        
    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def changeColor(self,position): 
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

#inspired in part by Skrx's answer in stack overflow
class TextEntry():
    def __init__ (self, text, pos, font, base_color, active_color, active):
        self.font = font
        self.x_pos, self.y_pos = pos[0], pos[1]
        self.base_color, self.active_color = base_color, active_color
        self.text_input = text
        self.active = active
        self.text = self.font.render(self.text_input, True, 'black')
        self.rect = pg.Rect(pos[0],pos[1],self.text.get_width()+20,self.text.get_height())
        
    def update(self, screen):
        color = self.active_color if self.active else self.base_color
        pg.draw.rect(screen, color, self.rect)
        screen.blit(self.text, (self.x_pos,self.y_pos))
        
    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        else:
            return False
    def get_text(self,key_event,text):
        if self.active:
            if key_event == pg.K_RETURN:
                text = text[:-1]
                print("got it")
                self.active = False
            elif key_event == pg.K_BACKSPACE:
                if len(text) > 0:
                    text = text[:-1]
                    print("here")
            else:
                text += key_event.unicode
        return text
    
def paragraph_blit(surface,text,pos,font,m_width,m_height,**options): #allows for placing paragraphs of text
    #Basis from Ted Klein on stack overflow    
    color = pg.Color('black')
    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]
    max_width = m_width
    x,y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word,0, color)
            word_width, word_height = word_surface.get_size()
            if word == '\n':
                y += word_height
                continue
            if x + word_width >= max_width:
                x = pos[0]
                y += word_height
            surface.blit(word_surface, (x,y))
            x += word_width + space
        x = pos[0]
        y += word_height
        
class Text:
    def __init__(self, text, pos, fontsize,**options):
        self.text = text
        self.pos = pos
        
        self.fontname = None
        self.fontsize = fontsize
        self.fontcolor = pg.Color('black')
        self.set_font() 
        self.render()
        
    def set_font(self):
        self.font = pg.font.Font(self.fontname, self.fontsize)
    def render(self):
        self.img = self.font.render(self.text, True, self.fontcolor)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos
    def draw(self, screen):
        screen.blit(self.img, self.rect)

#From Rabbid76 on stackoverflow        
class DropDown():
        def __init__(self, color_menu, color_option, x, y, w, h, font, main, options):
            self.color_menu = color_menu
            self.color_option = color_option
            self.rect = pg.Rect(x,y,w,h)
            self.font = font
            self.main = main
            self.options = options 
            self.menu_active = False
            self.draw_menu = False
            self.active_option = -1
            
        def draw(self, screen):
            pg.draw.rect(screen, self.color_menu[1 if self.menu_active else 0],self.rect,0)
            msg = self.font.render(self.main,1,(0,0,0))
            screen.blit(msg,msg.get_rect(center = self.rect.center))
            
            if self.draw_menu:
                for i, text in enumerate(self.options):
                    rect = self.rect.copy()
                    rect.y += (i+1) * self.rect.height
                    pg.draw.rect(screen,self.color_option[1 if i == self.active_option else 0],rect, 0)
                    msg = self.font.render(text,1,(0,0,0))
                    screen.blit(msg,msg.get_rect(center = rect.center))
        
        def update(self, position):
            self.menu_active = self.rect.collidepoint(position)
            if self.menu_active and len(self.options)>0:
                self.draw_menu
            return self.menu_active
            
            self.active_option = -1
            for i in range(len(self.options)):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                if rect.collidepoint(position):
                    self.active_option = i
                    break
            if not self.menu_active and self.active_option == -1:
                self.draw_menu = False
                
       
                    
            