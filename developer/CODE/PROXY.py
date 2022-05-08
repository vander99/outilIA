from re                                   import T
from tkinter                              import *
from matplotlib                           import pyplot            as plt
from matplotlib.backends.backend_tkagg    import FigureCanvasTkAgg
from SetResult                            import *
from os                                   import listdir
from os.path                              import isfile, join
from PIL                                  import Image, ImageTk
from ExtractData                          import *

import numpy                  as np
import pandas                 as pd
import tkinter.scrolledtext   as st

import sklearn.utils
import sklearn.tree

t = np.linspace(0,380,dtype=int)


def main():
	root = Tk()
	gui = Window(root)
	gui.root.mainloop()
	return None

class Window:
	def __init__(self, root):
		self

		self.root                                   = root
		self.root.title("Prediction production")

		self.with_train                             = IntVar()
		self.with_test                              = IntVar()

		self.figure                                 = plt.figure(figsize = (5,4), dpi = 100)
		self.axe                                    = self.figure.add_subplot(111)

		self.case                                   = StringVar(self.root,value='PROD(GPRi,GIP,WGV)')
		self.showcol                                = 'Field GPR'
		self.GPRi                                   = 1600
		self.WGV                                    = 156690
		self.GIP                                    = 1131000

		print('FUNCTIONS SEATING')
		self.f,self.fwm,self.fwp,self.df_train,self.df_test,self.fwm,self.fwp,self.ErrTcst,self.ErrDec,self.ErrWm,self.ErrWp = SetResult(root,'PROD(GPRi,GIP,WGV)')
		print('FUNCTIONS ARE READY')
  
		self.GPRi_current_value                     = DoubleVar()
		self.GIP_current_value                      = DoubleVar()
		self.WGV_current_value                      = DoubleVar()
		
  		#---------------------------------------------------------------------------------------
		#Widget declaration --------------------------------------------------------------------
		#---------------------------------------------------------------------------------------

		# GPRi
		Label(self.root, text = "Flow Rate").grid(row=0, column=0)
		self.GPRi_entry = Entry(self.root, width = 10,bg='#defaee')
		self.GPRi_entry.grid(row=0, column = 1)


		# WGV
		Label(self.root, text = "WGV").grid(row=1, column=0)
		self.WGV_entry = Entry(self.root, width = 10,bg='#defaee')
		self.WGV_entry.grid(row=1, column=1)
  
		# GIP
		Label(self.root, text = "GIP").grid(row=2, column=0)
		self.GIP_entry = Entry(self.root, width = 10,bg='#defaee')
		self.GIP_entry.grid(row=2, column=1)

		#Logo
		canvas = tk.Canvas(self.root, width=10, height=5)
		canvas.grid()

		logo = Image.open("storengy.png")
		logo = ImageTk.PhotoImage(logo)
		logo_label = Label(image=logo)
		logo_label.image = logo
		logo_label.grid(column=3, row=31)


		#case
		OptionList = [
					"INJ(GIRi,WGV)",
					"INJ(GIRi,GIP,WGV)",
					"PROD(GPRi,WGV)",
					"PROD(GPRi,GIP,WGV)"
					] 

		variable = StringVar(self.root)
		variable.set(OptionList[0])
		opt = tk.OptionMenu(
      				  self.root, 
                      self.case,
                      *OptionList,
                      command=self.changemodel)
		opt.config(font=('Helvetica', 12), bg= '#d8ff9b')
		opt.grid(row=0, column=2)
			

		#Train
		Train_checkbox = Checkbutton(self.root, 
									text='Show Train', 
									variable=self.with_train, 
									onvalue=1, 
									offvalue=0,
									command=self.display )
		Train_checkbox.grid(row=4, column=2)

		#Test
		Test_checkbox = Checkbutton(self.root, 
									text='Show Test', 
									variable=self.with_test, 
									onvalue=1, 
									offvalue=0,
									command=self.display )
		Test_checkbox.grid(row=4, column=1)

		#slider
		Label(self.root, text = "Flow Rate :").grid(row=10, column=0,sticky='w')
		GPRi_slider = Scale(
      						self.root,
							from_= 500,
							to   = 3500,
         					length=350,
                      		orient='horizontal',
                        	command=self.slider_changed,
    						variable=self.GPRi_current_value
          					)
		GPRi_slider.grid(row=10, column=0)
		Label(self.root, text = "WGV :").grid(row=11, column=0,sticky='w')
		WGV_slider = Scale(
      						self.root,		
							from_= 100000,
							to   = 300000,
							length=350,
                      		orient='horizontal',
                        	command=self.slider_changed,
    						variable=self.WGV_current_value
          					)
		WGV_slider.grid(row=11, column=0)
		self.root.bind("<Return>", self.slider_changed)

		Label(self.root, text = "GIP:").grid(row=12, column=0,sticky='w')
		WGV_slider = Scale(
							self.root,		
							from_= 1130000,
							to   = 1141000,
							length=350,
							orient='horizontal',
							command=self.slider_changed,
							variable=self.GIP_current_value
							)
		WGV_slider.grid(row=12, column=0)
		self.root.bind("<Return>", self.slider_changed)
			
  
		# Update Button
		button1 = Button(
      					self.root, 
                   		text="Predict", 
                     	command = self.update_values,
                      	bg = '#a8cceb', 
                       	activebackground='#a8cceb'
                        )
  
		button1.grid(row=4, column=0)
		self.root.bind("<Return>", self.update_values)
		self.plot_values()
		pass
		
		
	#--------------------------------------------------------------------------------------------------	
	#functions ----------------------------------------------------------------------------------------	
	#--------------------------------------------------------------------------------------------------

	def changemodel(self,event=None):
		print('FUNCTIONS SEATING')
		self.f,self.fwm,self.fwp,self.df_train,self.df_test,self.fwm,self.fwp,self.ErrTcst,self.ErrDec,self.ErrWm,self.ErrWp = SetResult(self.root,self.case.get())
		print('FUNCTIONS ARE READY')
		axe1 = self.axe
		axe1.clear()
		self.plot_values()
		chart = FigureCanvasTkAgg(self.figure, self.root)
		chart.get_tk_widget().grid(row = 8, column = 0)
		print("The model is chaged to  : ", self.case.get())
		return None




	def display(self):
     
		if self.case.get() == "PROD(GPRi,GIP,WGV)":
			self.showcol   = 'Field GPR'
		elif self.case.get() == "PROD(GPRi,WGV)":
			self.showcol   = 'Field GPR'
		elif self.case.get() == "INJ(GIRi,WGV)":
			self.showcol   = 'Field GIR'
		elif self.case.get() == "INJ(GIRi,GIP,WGV)":
			self.showcol   = 'Field GIR'
		else:
			self.showcol   = 'Field GPR'

		print("display, The plot contain: ", self.showcol  )

		if self.with_train.get() or self.with_test.get() :
			axe1 = self.axe
			axe1.clear()
			if self.with_train.get() and self.with_test.get():
				axe1.clear()
				print("Plot TEST")
				for i in range(len(self.df_test)): axe1.plot(self.df_test[i].loc[:,self.showcol],'--r')
    
				print("Plot TRAIN")
				for i in range(len(self.df_train)): axe1.plot(self.df_train[i].loc[:,self.showcol],'--k')

			if self.with_train.get() and not self.with_test.get() :
				axe1.clear()
				self.plot_values()
				print("Plot TRAIN")
				for i in range(len(self.df_train)): axe1.plot(self.df_train[i].loc[:,self.showcol],'--k')
    
			if not self.with_train.get() and self.with_test.get():
				axe1.clear()
				self.plot_values()
				print("Plot TEST")
				for i in range(len(self.df_test)): axe1.plot(self.df_test[i].loc[:,self.showcol],'--r')
				
    
			chart = FigureCanvasTkAgg(self.figure, self.root)
			chart.get_tk_widget().grid(row = 8, column = 0)
			
		else:
			axe1 = self.axe
			axe1.clear()
			self.plot_values()
			chart = FigureCanvasTkAgg(self.figure, self.root)
			chart.get_tk_widget().grid(row = 8, column = 0)
			
		
		
	
 
 
 	
       
	def update_values(self, event=None):
		self.GPRi = float(self.GPRi_entry.get())
		self.WGV = float(self.WGV_entry.get())
		self.GIP = float(self.GIP_entry.get())
		self.plot_values()
		return None



	def slider_changed(self,event):
		self.GPRi = float(self.GPRi_current_value.get())
		self.WGV = float(self.WGV_current_value.get())
		self.GIP = float(self.GIP_current_value.get())
		self.plot_values()
  
		return None
 
 
    #///////////////////////////////////////////////////////////////////
    #//////////////////////////////////////////////////////////////////
    #PLOT
    #/////////////////////////////////////////////////////////////////
    #////////////////////////////////////////////////////////////////
 
	def plot_values(self):
		
		if self.case.get() == "PROD(GPRi,GIP,WGV)":
			Tcst,y = self.f(self.GPRi,self.GIP,self.WGV)
			self.showcol   = 'Field GPR'
		elif self.case.get() == "PROD(GPRi,WGV)":
			Tcst,y = self.f(self.GPRi,self.WGV)
			self.showcol   = 'Field GPR'
		elif self.case.get() == "INJ(GIRi,WGV)":
			Tcst,y = self.f(self.GPRi,self.WGV)
			self.showcol   = 'Field GIR'
		elif self.case.get() == "INJ(GIRi,GIP,WGV)":
			Tcst,y = self.f(self.GPRi,self.GIP,self.WGV)
			self.showcol   = 'Field GIR'
		else:
			Tcst,y = self.f(self.GPRi,self.WGV)
			self.showcol   = 'Field GIR'


		print("plot_values, The plot contain: ", self.showcol)
		volume_prod = sum(y)
  
		print(Tcst)
		print(volume_prod)
  
		plt.grid()
		axe1 = self.axe
		axe1.clear()
		axe1.plot(y, 'g')
  
  
		if self.with_train.get() or self.with_test.get() :
			
			if self.with_train.get() and self.with_test.get():

				for i in range(len(self.df_test)): axe1.plot(self.df_test[i].loc[:,self.showcol],'--r')

				for i in range(len(self.df_train)): axe1.plot(self.df_train[i].loc[:,self.showcol],'--k')

			if self.with_train.get() and not self.with_test.get() :

				for i in range(len(self.df_train)): axe1.plot(self.df_train[i].loc[:,self.showcol],'--k')

			if not self.with_train.get() and self.with_test.get():
       
				for i in range(len(self.df_test)): axe1.plot(self.df_test[i].loc[:,self.showcol],'--r')

		text_area = st.ScrolledText(self.root,
							width = 35,
							height = 8,
							font = ("Times New Roman",
									8),
       						background="#b8fac4")

		text_area.grid(row = 8 ,column = 1, ipady = 142, rowspan=1,columnspan=2,sticky = 'n')

		# Inserting Text which is read only
		txt = f'''
\n
Periode of the constante part Tcst : \n 
{str(int(Tcst))} Days\n
\n
injected volume : \n
{str(int(self.WGV))} kSm3
\n
Water produced : \n
{self.fwp(self.GPRi,self.GIP,self.WGV)[0]} m3
\n
max Water production : \n
{self.fwm(self.GPRi,self.GIP,self.WGV)[0]} m3/d
\n
Err of Tcst prediction : \n
{self.ErrTcst}
\n 
Err of decreasing part prediction : \n
{self.ErrDec}
\n 
Err of water produced prediction : \n
{self.ErrWp}
\n 
Err of max water production prediction : \n
{self.ErrWm}
\n 

				'''
                              
		text_area.insert(END,txt)

		# Making the text read only
		text_area.configure(state ='disabled')

		chart = FigureCanvasTkAgg(self.figure,self.root)
		chart.get_tk_widget().grid(row = 8, column = 0)


		return None

	

	
	pass

main()
                        
        