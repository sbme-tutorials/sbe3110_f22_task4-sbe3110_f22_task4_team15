import numpy as np



class Image:


    image_size =235

    def __init__(self,x=[[0]],mag_x=0,phase_x=0,y=0):
        self.arr_size=min(len(x), len(x[0]))
        self.fourier_transformed_image=np.fft.fftshift(np.fft.fft2(x,s=(self.arr_size,self.arr_size)))
        self.fourier_transformed_image_magnitude=np.abs(self.fourier_transformed_image)
        self.fourier_transformed_image_phase=np.angle(self.fourier_transformed_image)
        self.mag_x=mag_x
        self.phase_x=phase_x
        self.mag_y=self.phase_y=y
        self.masked_mag=self.fourier_transformed_image_magnitude
        self.masked_phase=self.fourier_transformed_image_phase


    def coordinates_to_indices(self,x,y,width,height,xreference,yrefernce):
        y_indx1= self.arr_size*(y-yrefernce)/self.image_size
        y_indx2= self.arr_size*(y+height-yrefernce)/self.image_size
        x_indx1= self.arr_size*(x-xreference)/self.image_size
        x_indx2= self.arr_size*(x+width-xreference)/self.image_size

        return y_indx1,y_indx2,x_indx1,x_indx2


    def Mask_magnitude(self,x,y,width,height,mode): 

        y_indx1,y_indx2,x_indx1,x_indx2=self.coordinates_to_indices(x,y,width,height,self.mag_x,self.mag_y)

        self.masked_mag=self.fourier_transformed_image_magnitude.copy()
        if mode==1:
            self.masked_mag[int(y_indx1):int(y_indx2),int(x_indx1):int(x_indx2)]=1
        else:
            self.masked_mag.fill(1)
            self.masked_mag[int(y_indx1):int(y_indx2),int(x_indx1):int(x_indx2)]= self.fourier_transformed_image_magnitude[int(y_indx1):int(y_indx2),int(x_indx1):int(x_indx2)]
  
        return self.masked_mag



    def Mask_phase(self,x,y,width,height,mode):

        y_indx1,y_indx2,x_indx1,x_indx2=self.coordinates_to_indices(x,y,width,height,self.phase_x,self.phase_y)

        self.masked_phase=self.fourier_transformed_image_phase.copy()
        if mode==1:
            self.masked_phase[int(y_indx1):int(y_indx2),int(x_indx1):int(x_indx2)]=1
        else:
           self.masked_phase.fill(1)
           self.masked_phase[int(y_indx1):int(y_indx2),int(x_indx1):int(x_indx2)]= self.fourier_transformed_image_phase[int(y_indx1):int(y_indx2),int(x_indx1):int(x_indx2)]
        return self.masked_phase



    def reconstruct(self,image2,x,y,width,height,x2,y2,width2,height2,mode):

        new_mag=np.array([])
        new_phase=np.array([])

        if ( all( self.mag_x+self.image_size>m> self.mag_x for m in (x,x+width)) and all( self.mag_y+self.image_size>m > self.mag_y for m in (y,y+height))):
            new_mag=self.Mask_magnitude(x,y,width,height,mode)

        if ( all(image2.mag_x+self.image_size>m >image2.mag_x for m in (x,x+width)) and all(image2.mag_y+self.image_size>m >image2.mag_y for m in (y,y+height))):
            new_mag=image2.Mask_magnitude(x,y,width,height,mode)

        if ( all( self.phase_x+self.image_size>m> self.phase_x for m in (x2,x2+width2)) and all( self.phase_y+self.image_size>m > self.phase_y for m in (y2,y2+height2))):
            new_phase=self.Mask_phase(x2,y2,width2,height2,mode)

        if ( all( image2.phase_x+self.image_size>m> image2.phase_x for m in (x2,x2+width2)) and all( image2.phase_y+self.image_size>m > image2.phase_y for m in (y2,y2+height2))):
            new_phase=image2.Mask_phase(x2,y2,width2,height2,mode)
        
       
        if (len(new_mag)!=0 and len(new_phase)!=0):
            if (self.arr_size!=1 and image2.arr_size !=1):
              m=min(self.arr_size, image2.arr_size)
            else:
              m=max(self.arr_size, image2.arr_size)

            new_mag=new_mag[:m , :m]
            new_phase=new_phase[:m , :m]

        else:

            new_mag=np.ones((500,500))
            new_phase=np.zeros((500,500))
        
        complex_f=new_mag* np.exp(1j* new_phase)
        reconstructed=np.fft.ifft2(complex_f)
        return reconstructed
