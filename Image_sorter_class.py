

from tkinter import *
from tkinter import ttk

from PIL import ImageTk, Image
import os
from tqdm import *
import numpy as np
import logging
import sys
from logging.handlers import TimedRotatingFileHandler


class image_viewer:


    FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
    LOG_FILE = "image_sorter.log"
    def __init__(self,base_path,folder_names):
        self.root = Tk()

        self.content = ttk.Frame(self.root)
        self.frame = ttk.Frame(self.content, borderwidth=5, relief="ridge", width=1000, height=600)
        self.root.title("Image Sorter")
        self.folder_names = folder_names
        self.file_list=[]
        self.my_logger = self.get_logger("image_sorter_class")
        self.lista=[]
        self.base_path = self.check_base_path(base_path)
        self.numClasses= len(self.folder_names)
        self.folderN=[[] for i in range(self.numClasses)]
        self.create_folders()
        self.file_list=self.load_images(self.base_path)
        self.font_height = 20
        self.num_of_buttons_per_row=8;
        self.class_button_width=15
        self.class_button_height=3
        self.image_height=600
        self.image_width=1000;
        self.build_geometry()

        for i in tqdm(self.file_list):
            self.lista.append(ImageTk.PhotoImage(Image.open(i).resize((self.image_width, self.image_height),Image.ANTIALIAS)))
        self.label=None
        self.button_for=None
        self.button_back =None
        self.button_exit =None
        self.my_logger.debug("initializing class")
        self.my_logger.debug(str(folder_names)[1:-1])
        self.my_logger.debug("name of folders="+"path= "+base_path)
        self.current_img_no=0

    def get_console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.FORMATTER)
        return console_handler

    def get_file_handler(self):
        file_handler = TimedRotatingFileHandler(self.LOG_FILE, when='midnight')
        file_handler.setFormatter(self.FORMATTER)
        return file_handler

    def get_logger(self,logger_name):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self.get_console_handler())
        logger.addHandler(self.get_file_handler())
        logger.propagate = False
        return logger


    def create_folders(self):
        self.new_path = self.base_path.replace('images', 'images_sorted')
        if not os.path.exists(self.new_path):
            self.my_logger.debug("creating folder: "+self.new_path)
            os.mkdir(self.new_path)
        for i in self.folder_names:
            k = self.base_path.replace('images', os.path.join('images_sorted', i))
            if not os.path.exists(k):
                self.my_logger.debug("creating folder: " + k)
                os.mkdir(k)



    def load_images(self,file_path):
        if "images" not in file_path:
            self.my_logger.error("images must be put in the 'images' folder")
            sys.exit(1)
        else:
            files=os.listdir(file_path)
            file_list=[]
            self.my_logger.debug("loading images")
            for i in files:
                if os.path.isfile(os.path.join(file_path,i)) and ('png' in i or 'jpg' in i or 'jpeg' in i):
                    file_list.append(os.path.join(file_path,i))
            if (len(file_list)==0):
                self.my_logger.error("no images found")
                sys.exit(1)
            else:
                return file_list

    def start_gui(self):
        self.label = Label(image=self.lista[0])
        self.label.grid(row=0, column=0, columnspan=self.num_of_buttons_per_row)
        self.set_forward_button()
        self.set_back_button(True)
        self.set_exit_button()
        self.buttonList=[];
        self.set_class_buttons()
        self.root.mainloop()



    def smista(self):
        set_list=[]
        for i in self.folderN:
            set_list.append(list(set(i)))

         #sort  images in folder
        for i,j in zip(set_list,self.folder_names):
            for k in i:
                print(k)
                new_name=k.replace('images',os.path.join('images_sorted',j))

                if not os.path.exists(new_name):
                    os.rename(k,new_name)
                else:
                    continue


    def cartellaN(self,numFolder):
        self.my_logger.debug("selected folder number "+str(numFolder))
        self.label.grid_forget()
        if self.current_img_no==len(self.lista)-1:
            self.my_logger.info("image number"+self.current_img_no+"is the last image")
            self.folderN[numFolder].append(self.file_list[self.current_img_no])
            self.my_logger.info("added to folder"+self.folderN[numFolder])
            self.my_logger.info("appendend image "+str(self.current_img_no))
        elif self.current_img_no>=len(self.lista):
            self.my_logger.info("reached last image, cannot fo further")
        else:
            if self.current_img_no >= 0:
                self.folderN[numFolder].append(self.file_list[self.current_img_no])
            self.my_logger.info("added image number "+str(self.current_img_no))
            self.current_img_no=self.current_img_no+1
            self.label = Label(image=self.lista[self.current_img_no])
            self.my_logger.debug("going to next image "+str(self.current_img_no))
            self.label.grid(row=1, column=0, columnspan=self.num_of_buttons_per_row)
            self.set_class_buttons()
        self.set_forward_button()
        self.set_back_button()
        self.set_exit_button()

    def set_forward_button(self, is_disabled=False):
        if is_disabled:
            self.button_forward = Button(self.root,height=self.class_button_height, width=self.class_button_width, text="Forward",
                                         command=lambda: self.forward(), state=DISABLED)
        else:
            self.button_forward = Button(self.root,height=self.class_button_height, width=self.class_button_width, text="Forward",
                                         command=lambda: self.forward())
        self.button_forward.grid(row=5, column=2)

    def set_back_button(self, is_disabled=False):
        if is_disabled:
            self.button_back = Button(self.root, height=self.class_button_height, width=self.class_button_width, text="Back", command=lambda: self.back(),
                                      state=DISABLED)
        else:
            self.button_back = Button(self.root, height=self.class_button_height, width=self.class_button_width, text="Back", command=lambda: self.back())
        self.button_back.grid(row=5, column=0)

    def set_exit_button(self):
        self.button_exit = Button(self.root, height=self.class_button_height, width=self.class_button_width, text="Exit",
                                  command=self.root.quit)
        self.button_exit.grid(row=5, column=1)

    def forward(self):
        self.current_img_no=self.current_img_no+1
        self.my_logger.info("current image: "+str(self.current_img_no))
        self.label.grid_forget()
        for i in self.buttonList:
            i.grid_forget()
        if self.current_img_no <= len(self.file_list)-1:
            self.label = Label(image=self.lista[self.current_img_no])
        self.label.grid(row=0, column=0, columnspan=self.num_of_buttons_per_row)
        self.my_logger.info("going forward to: "+str(self.current_img_no))

        if self.current_img_no == len(self.file_list):
            self.my_logger.info("tried to go forward after the last image")
            self.set_forward_button(True)
        else:
            self.set_forward_button()

        self.set_back_button()
        self.set_exit_button()
        self.set_class_buttons()

    def back(self):
        self.current_img_no=self.current_img_no-1
        for i in self.buttonList:
            i.grid_forget()
        self.my_logger.info("going backward to: "+str(self.current_img_no))
        if self.current_img_no <= -1:
            self.my_logger.info("trying to access image number -1")
            self.current_img_no=self.current_img_no+1;
            self.set_back_button(True)

        else:
            self.label.grid_forget()
            self.set_back_button()
            self.label = Label(image=self.lista[self.current_img_no])
            self.label.grid(row=1, column=0, columnspan=self.num_of_buttons_per_row)
            self.set_forward_button()
            self.set_class_buttons()

    def set_class_buttons(self):
        for i in range(self.numClasses):
            addedRow = int(np.floor(i / self.num_of_buttons_per_row));
            if (addedRow == 0):
                myColumn = i;
            else:
                myColumn = i - self.num_of_buttons_per_row * addedRow;
            self.buttonList.append(Button(self.root, height=self.class_button_height, width=self.class_button_width, text=self.folder_names[i],
                                          command=lambda i=i: self.cartellaN(i)))
            self.buttonList[-1].grid(row=6 + addedRow, column=myColumn,sticky="nsew")

    def check_base_path(self, base_path):
        if os.path.isdir(base_path):
            return base_path
        else:
            self.my_logger.error("folder "+base_path+" not found")
            sys.exit(1)

    def build_geometry(self):
        width = 1500
        num_rows=np.ceil(len(self.folder_names)/self.num_of_buttons_per_row)
        height = int(self.image_height+100 + np.ceil(( num_rows * self.class_button_height*self.font_height)))
        self.root.geometry(str(width) + "x" + str(height))

