# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 11:06:01 2016

@author: 19g
"""
import matplotlib.pyplot as plt
import matplotlib.colors as mpl_c
import numpy as np


class scans:
    """
    A class for a collection of scans
    """
    def __init__(self,scans_dict=None):        
        self.scans=scans_dict
        if scans_dict!=None:
          self.num_scans=len(scans_dict)

    def update(self,scans_dict):
        """
        update the scans_dict to incldue the dictionary scans_dict
        This will update any scans that are already in the class and will append those that are not
        """
        self.scans.update(scans_dict)
        self.num_scans=len(scans_dict)
    
    def scans_check(self):
        """
        check to see if the scans are populated
        """
        if self.scans==None:
            raise RuntimeError('There must be at lest one scan') 
    def waterfall(self,x='e',y='detector',label_column='h',offset=5,fmt='b-',legend=False):
        """
        create a waterfall plot of all the scans in the collection
        """
        self.scans_check()  
        fh=plt.figure()
        plt.hold(True)
        for idx,scan_num in enumerate(self.scans.keys()):        
            xin=self.scans[scan_num].data[x]
            yin=self.scans[scan_num].data[y]
            avg_label_val=self.scans[scan_num].data[label_column].mean()
            label_str="%s =%1.3f"%(label_column,avg_label_val)
            plt.plot(xin,yin+offset*idx,fmt,label=label_str)
            plt.xlabel(x)
            plt.ylabel(y)
        if legend:
            plt.legend()    
        plt.show(block=False)
    
    def mean_col(self,col=None):
        """ 
        take the mean of a given column in every data set
        requires a column name
        """
        col_mean=np.zeros(self.num_scans)        
        for idx, scan_num in enumerate(self.scans.keys()):
            col_mean[idx]=self.scans[scan_num].data[col].mean()
        return col_mean 
            
    def pcolor(self,x=None,z='detector',y=None,clims=None,color_norm=None,cmap='jet'):
        """
        create a pcolor for a group of scans.  The y direction is always waht varies between scans.
        
        """
        self.scans_check()
        fh=plt.figure()
        #calculate y spacing
        meany=self.mean_col(col=y)
        biny=np.zeros(len(meany)+1)  # generate an array for bin boundaries of the y axis     
        biny[1:-1]=(meany[:-1]+meany[1:])/2  #generate the bin boundaries internal to the array
        biny[0]=2*meany[0]-biny[1] # generate the first bin boundary to be the same disatance from the mean as the second bin boundary
        biny[-1]=2*meany[-1]-biny[-2] # generate the last bin boundary to be the same diastance from the mean as the next to last.
        if clims==None:        
          #calcualte intensity range        
          intens_max=0.
          intens_min=1.
          for idx, scan_num in enumerate(self.scans.keys()):
              maxz=self.scans[scan_num].data[z].max()
              minz=self.scans[scan_num].data[z].min()
              if maxz>intens_max:
                  intens_max=maxz
              if (minz<intens_min)&(minz>0):
                  intens_min=minz
          #print(intens_min,intens_max) 
        else:
            intens_max=clims[1]
            intens_min=clims[0]
        for idx, scan_num in enumerate(self.scans.keys()):
            meansx=self.scans[scan_num].data[x]
            zvals=self.scans[scan_num].data[z]
            yvals=np.array([biny[idx],meany[idx],biny[idx+1]])
            xvals=np.zeros(len(meansx)+1)
            xvals[1:-1]=(meansx[:-1]+meansx[1:])/2.
            xvals[0]=2*meansx[0]-xvals[1]
            xvals[-1]=2*meansx[-1]-xvals[-2]
            xmat=np.vstack((xvals,xvals,xvals))
            ymat=np.tile(yvals,(len(xvals),1)).T
            zmat=np.vstack((zvals,zvals))
            if color_norm=='log':
                plt.pcolor(xmat,ymat,zmat,norm=mpl_c.LogNorm(vmin=intens_min,vmax=intens_max),cmap=cmap)
            else:            
                plt.pcolor(xmat,ymat,zmat,vmin=intens_min,vmax=intens_max,cmap=cmap)
            
            
        plt.xlabel(x)
        plt.ylabel(y)         
        plt.colorbar()        
        plt.show(block=False)
            
        #return intens_min, intens_max          
            
            
            
            