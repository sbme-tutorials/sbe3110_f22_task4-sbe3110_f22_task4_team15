import numpy as np
import matplotlib.pyplot as plt
import math
import skimage.io 
import cv2
import numpy as np 
import base64
import io
import PIL.Image as Image
import base64

class Fourier2d:




    def __init__(self,x=[[0]],mag_x=0,phase_x=0,y=0):
        self.size=min(len(x), len(x[0]))
        self.fourier_transformed_image=np.fft.fftshift(np.fft.fft2(x,s=(self.size,self.size)))
        self.fourier_transformed_image_magnitude=np.abs(self.fourier_transformed_image)
        self.fourier_transformed_image_phase=np.angle(self.fourier_transformed_image)
        self.mag_x=mag_x
        self.phase_x=phase_x
        self.mag_y=self.phase_y=y
        self.masked_mag=self.fourier_transformed_image_magnitude
        self.masked_phase=self.fourier_transformed_image_phase




    def save_plts(self,image_file_name1,image_file_name2):
        fig = plt.figure(figsize=(4, 4))
        plt.imshow(np.log(self.fourier_transformed_image_magnitude))
        plt.savefig(image_file_name1)
        plt.imshow(self.fourier_transformed_image_phase)
        plt.savefig(image_file_name2)





    def Mask_magnitude(self,x,y,width,height): 
        y_indx1= self.size*(y-self.mag_y)/300
        y_indx2= self.size*(y+height-self.mag_y)/300
        x_indx1= self.size*(x-self.mag_x)/300
        x_indx2= self.size*(x+width-self.mag_x)/300

        self.masked_mag=self.fourier_transformed_image_magnitude.copy()
        self.masked_mag[int(y_indx1):int(y_indx2),int(x_indx1):int(x_indx2)]=1
        print(int(y_indx1))
        print(y_indx2)
        print(x_indx1)
        print(x_indx2)
        return self.masked_mag



    def Mask_phase(self,x,y,width,height):
        y_indx1= self.size*(y-self.phase_y)/300
        y_indx2= self.size*(y+height-self.phase_y)/300
        x_indx1= self.size*(x-self.phase_x)/300
        x_indx2= self.size*(x+width-self.phase_x)/300

        self.masked_phase=self.fourier_transformed_image_phase.copy()
        self.masked_phase[int(y_indx1):int(y_indx2),int(x_indx1):int(x_indx2)]=1
      
        return self.masked_phase



    def reconstruct(self,image2,x,y,width,height,x2,y2,width2,height2):

        new_mag=np.array([])
        new_phase=np.array([])

        if ( all( self.mag_x+300>m> self.mag_x for m in (x,x+width)) and all( self.mag_y+300>m > self.mag_y for m in (y,y+height))):
            print("hena1")
            new_mag=self.Mask_magnitude(x,y,width,height)


        if ( all(image2.mag_x+300>m >image2.mag_x for m in (x,x+width)) and all(image2.mag_y+300>m >image2.mag_y for m in (y,y+height))):
            print("hena2")
            new_mag=image2.Mask_magnitude(x,y,width,height)

        if ( all( self.phase_x+300>m> self.phase_x for m in (x2,x2+width2)) and all( self.phase_y+300>m > self.phase_y for m in (y2,y2+height2))):
            print("hena3")
            new_phase=self.Mask_phase(x2,y2,width2,height2)



        if ( all( image2.phase_x+300>m> image2.phase_x for m in (x2,x2+width2)) and all( image2.phase_y+300>m > image2.phase_y for m in (y2,y2+height2))):
            print("hena4")
            new_phase=image2.Mask_phase(x2,y2,width2,height2)

        if (len(new_mag)!=0 and len(new_phase)!=0):
            fig = plt.figure(figsize=(4, 4))
            complex_f=new_mag* np.exp(1j* new_phase)
            reconstructed=np.fft.ifft2(complex_f)
            plt.imshow(np.abs(reconstructed), cmap='gray')
            plt.savefig('reconstructed.jpg') 