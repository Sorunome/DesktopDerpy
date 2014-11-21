#!/usr/bin/env python3
## -*- coding: utf-8 -*-
import os,cairo,random
from gi.repository import Gtk,Gdk,GObject

PROGDIR = os.path.dirname(os.path.realpath(__file__))+'/'

def addMenuItem(menu,item,fn):
	mItem = Gtk.MenuItem(item)
	mItem.show()
	menu.append(mItem)
	mItem.connect('activate',fn)

class Derpy:
	def __init__(self):
		
		self.window = Gtk.Window()
		self.window.set_decorated(False)
		self.window.set_keep_above(True)
		self.window.hide()
		self.window.set_skip_taskbar_hint(True)
		
		if self.window.get_screen().get_rgba_visual() != None and self.window.get_screen().is_composited():
			self.window.set_visual(self.window.get_screen().get_rgba_visual())
			self.window.set_app_paintable(True)
			self.window.connect('draw',self.area_draw)
		else:
			print('no transparency support')
		
		
		self.width = 106
		self.height = 94
		self.xVel = 0
		self.yVel = 0
		self.action = 'stand'
		self.direction = 'right'
		self.extra = ''
		self.wing = False
		self.sleep = False
		self.drag = False
		self.xPos = (Gdk.Screen.get_default().get_width() / 2) - (self.width / 2)
		self.yPos = (Gdk.Screen.get_default().get_height() / 2) - (self.height / 2)
		
		
		self.wingActions = ['stand','walking']
		self.actionsStand = ['hover','hoverupsidedown','sleep','stand','sit']
		self.actionsMove = ['fly','flyupsidedown','walking','walking']
		self.actionsFly = ['fly','flyupsidedown']
		
		self.window.move(self.xPos,self.yPos)
		
		self.gif = Gtk.Image()
		
		self.set_image()
		
		
		self.window.add(self.gif)
		
		#add rightclick menu
		self.rightclickMenu = Gtk.Menu()
		#addMenuItem(rightclickMenu,'Backup',self.extra_backup)
		addMenuItem(self.rightclickMenu,'Sleep',self.sleep_toggle)
		addMenuItem(self.rightclickMenu,'Quit',self.show_quit_dialog)
		
		self.window.connect('button-press-event',self.button_press)
		self.window.connect('button-release-event',self.button_release)
		self.window.connect('motion-notify-event',self.mouse_move)
		
		
		self.window.show_all()
		
		
		self.set_draw_frame_timer()
		self.set_rand_event_timer()
		
	def button_press(self,widget,event):
		if event.button == 3:
			self.rightclickMenu.popup(parent_menu_shell = None,parent_menu_item = None,func = None,data = None,button = event.button,activate_time = event.time)
		if event.button == 1:
			self.x_offset = event.x_root - self.xPos
			self.y_offset = event.y_root - self.yPos
			self.xVel = 0
			self.yVel = 0
			self.xPos = event.x_root - 51
			self.yPos = event.y_root - 7
			self.action = 'drag'
			self.extra = ''
			self.drag = True
			self.set_image()
			self.draw_frame()
	def button_release(self,widget,event):
		if event.button == 1:
			self.drag = False
			self.xPos = event.x_root - self.x_offset
			self.yPos = event.y_root - self.y_offset
			if self.sleep:
				self.action = 'sleep'
				self.set_image()
			else:
				self.action = 'stand'
				self.set_rand_event_timer()
				self.set_draw_frame_timer()
				self.set_actions()
	def mouse_move(self,widget,event):
		if self.drag:
			self.xPos = event.x_root - 51
			self.yPos = event.y_root - 7
			self.draw_frame()
	def set_rand_event_timer(self):
		GObject.timeout_add(random.randint(3000,6000),self.rand_event)
	def set_draw_frame_timer(self):
		GObject.timeout_add(1000/30,self.draw_frame)
	def set_actions(self):
		if self.xVel < 0:
			self.direction = 'left'
		elif self.xVel > 0:
			self.direction = 'right'
		if self.xVel==0 and self.yVel==0:
			self.action = random.choice(self.actionsStand)
		elif self.yVel==0:
			self.action = random.choice(self.actionsMove)
		else:
			self.action = random.choice(self.actionsFly)
		if random.randint(1,10)==1:
			self.wing = not self.wing
		if self.action=='sit':
			self.extra = random.choice(['_long','_short'])
		else:
			self.extra = ''
		self.set_image()
	def rand_event(self):
		if not (self.sleep or self.drag):
			oldXVel = self.xVel
			oldYVel = self.yVel
			if random.randint(1,2)==1:
				self.xVel = random.choice([-2,0,2])
			if random.randint(1,2)==1:
				self.yVel = random.choice([-2,0,2])
			if oldXVel!=self.xVel or oldYVel!=self.yVel:
				self.set_actions()
			if not self.sleep:
				self.set_rand_event_timer()
		return False
	def sleep_toggle(self,widget):
		self.sleep = not self.sleep
		print(self.sleep)
		if self.sleep:
			self.yVel = 0
			self.xVel = 0
			self.action = 'sleep'
			self.extra = ''
			self.set_image()
		else:
			self.action = 'stand'
			self.set_rand_event_timer()
			self.set_draw_frame_timer()
			self.set_actions()
	def draw_frame(self):
		self.xPos += self.xVel
		if self.xPos < 0:
			self.xPos = 0
			self.xVel = 0
			if not self.drag:
				self.set_actions()
		elif self.xPos > (Gdk.Screen.get_default().get_width() - self.width):
			self.xPos = Gdk.Screen.get_default().get_width() - self.width
			self.xVel = 0
			if not self.drag:
				self.set_actions()
		self.yPos += self.yVel
		if self.yPos < 0:
			self.yPos = 0
			self.yVel = 0
			if not self.drag:
				self.set_actions()
		elif self.yPos > (Gdk.Screen.get_default().get_height() - self.height):
			self.yPos = Gdk.Screen.get_default().get_height() - self.height
			self.yVel = 0
			if not self.drag:
				self.set_actions()
		
		self.window.move(self.xPos,self.yPos)
		
		return not (self.sleep or self.drag)
	def area_draw(self,widget,cr):
		cr.set_source_rgba(0,0,0,0)
		cr.set_operator(cairo.OPERATOR_SOURCE)
		cr.paint()
		cr.set_operator(cairo.OPERATOR_OVER)
	def set_image(self):
		name = 'derpy_'+self.action
		if self.wing and (self.action in self.wingActions):
			name += '_wing'
		name += '_'+self.direction+self.extra+'.gif'
		self.window.resize(self.width,self.height)
		self.gif.set_from_file(PROGDIR+name)
		self.gif.show()
		print(PROGDIR+name)
	def show_quit_dialog(self,widget):
		dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.QUESTION,Gtk.ButtonsType.YES_NO,'Are you sure you want to quit Derpy?')
		response = dialog.run()
		dialog.destroy()
		if response == Gtk.ResponseType.YES:
			Gtk.main_quit()
	def main(self):
		Gtk.main()
if __name__ == '__main__':
	derpy = Derpy()
	derpy.main()