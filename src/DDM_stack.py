#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 12:33:38 2018

@author: anand
"""

import numpy as np
from scipy.interpolate import splrep, splev
from matplotlib.pylab import imread, imshow, subplot
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
import sys
import time
import os

class ImageStack(object):
    """A stack of images on disk with a name pattern like 'mydir\myfile_t{:03d}.tif'"""
    def __init__(self, pattern, Nbimages, t0=1):
        """The numbering can start at 0 or 1"""
        self.pattern = pattern
        self.t0 = t0
        self.Nbimages = Nbimages
        #get the images shape while checking that the last image do exist
        self.shape = imread(pattern.format(Nbimages-1+t0)).shape
        #for some monochrome image format, imread makes 4 channels out of one
        self.enforceMono = len(self.shape)>2
        if self.enforceMono:
            self.shape = self.shape[:-1]
            
    def __len__(self):
        return self.Nbimages
            
    def __getitem__(self, t):
        """returns the image at time t"""
        if t<0: t= len(self)+t
        assert t-self.t0 < self.Nbimages
        im = imread(self.pattern.format(t + self.t0))
        if self.enforceMono:
            im = im[...,0]
        return im

def spectrumDiff(im0, im1):
    """Compute the squared modulus of the 2D Fourier Transform of the difference between im0 and im1"""
    return np.abs(np.fft.fft2(im1-im0.astype(float)))**2


def timeAveraged(stack, dt, maxNCouples=100):
    """Does at most maxNCouples spectreDiff on regularly spaced couples of images. 
    Separation within couple is dt."""
    #Spread initial times over the available range
    increment = int(max([(len(stack)-dt)/maxNCouples, 1]))
    initialTimes = np.arange(0, len(stack)-dt, increment)
    #perform the time average
    avgFFT = np.zeros(stack.shape)
    for t in initialTimes:
        avgFFT += spectrumDiff(stack[t]/np.mean(stack[t]), stack[t+dt]/np.mean(stack[t+dt]))
    return avgFFT / len(initialTimes)

class RadialAverager(object):
    """Radial average of a 2D array centred on (0,0), like the result of fft2d."""
    def __init__(self, shape):
        """A RadialAverager instance can process only arrays of a given shape, fixed at instanciation."""
        assert len(shape)==2
        #matrix of distances
        self.dists = np.sqrt(np.fft.fftfreq(shape[0])[:,None]**2 +  np.fft.fftfreq(shape[1])[None,:]**2)
        #dump the cross
        self.dists[0] = 0
        self.dists[:,0] = 0
        #discretize distances into bins
        self.bins = np.arange(max(shape)/2+1)/float(max(shape))
        #number of pixels at each distance
        self.hd = np.histogram(self.dists, self.bins)[0]
    
    def __call__(self, im):
        """Perform and return the radial average of the specrum 'im'"""
        assert im.shape == self.dists.shape
        hw = np.histogram(self.dists, self.bins, weights=im)[0]
        return hw/self.hd

    def bins_out(self):
    	return self.bins    


def logSpaced(L, pointsPerDecade=15):
    """Generate an array of log spaced integers smaller than L"""
    nbdecades = np.log10(L)
    return np.unique(np.logspace(
        start=0, stop=nbdecades, 
        num=nbdecades * pointsPerDecade, 
        base=10, endpoint=False
        ).astype(int))


def ddm(stack, idts, maxNCouples=1000):
    """Perform time averaged and radial averaged DDM for given time intervals.
    Returns DDM"""
    ra = RadialAverager(stack.shape)
    DDM = np.zeros((len(idts), len(ra.hd)))
    #f = FloatProgress(min=0, max=len(idts))
    #display(f)
    for i, idt in enumerate(idts):
        DDM[i] = ra(timeAveraged(stack, idt, maxNCouples))
        #f.value = i
    return DDM
     
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
start_time = time.time()

NFRAMES = 1065#3268#10895#21790#5400#10895#43580#10613#10635#10636#10615#10611#10609#10603#10623#10621#10472#10612#8761      #actually index of last frame counting from 0
total_time_in_sec = 12#40#80#19.825608077099588#40#160#19.5612665#39.122533#40
#stack = ImageStack(u'/Users/anand/code/python-ddm/AY014 256-256 160sec 63X/AY014 256-256 160sec 63X{:05d}.tif',NFRAMES)
#outpath='/Users/anand/code/python-ddm/AY014 256-256 160sec 63X/a5norm_120/'
# stack = ImageStack(u'/Users/harnoorsingh/Desktop/DDM/DDM-dataset/AY014 256-256 40sec 63X/AY014 256-256 40sec 63X{:05d}.tif',NFRAMES)
# outpath='/Users/harnoorsingh/Desktop/DDM/DDM-output/output/'
stack = ImageStack(u'/Users/harnoorsingh/Desktop/DDM/DDM-dataset/AY014 256-256 40sec 63X/AY014 256-256 40sec 63X{:05d}.tif',NFRAMES)
outpath='/Users/harnoorsingh/Desktop/DDM/DDM-output/output/'

#a1  = timeAveraged(stack, 10)
#a2  = timeAveraged(stack, 50)
#a3  = timeAveraged(stack, 1000)
#a4  = timeAveraged(stack, 2000)
#ra = RadialAverager(stack.shape)


#plt.figure(figsize=(6,4))
#plt.plot(ra(a1),'ro-')
#plt.plot(ra(a2),'bo-')
#plt.plot(ra(a3),'go-')
#plt.plot(ra(a4),'yo-')

#plt.xscale('log')
#plt.yscale('log')
#plt.xlabel('q [px-1]')
#plt.ylabel('DDM')
#plt.show()

# Perform full analysis
pointsPerDecade = 15
maxNCouples = 500                                # 10 for fast evaluation, 300 for accurate analysis
idts = logSpaced(NFRAMES, pointsPerDecade)
freq = 1.0*NFRAMES/total_time_in_sec#243.275                                    # FrameRate [Hz]
print(freq)
dts  = idts/float(freq)
print("--- %s seconds ---" % (time.time() - start_time))
print(len(stack))
DDM = ddm(stack, idts, maxNCouples)               # Perform analysis
print("--- %s seconds ---" % (time.time() - start_time))

bins = RadialAverager(stack.shape).bins_out()
qv = bins[1:]                                     # units of inverse pixels
t_resc = np.zeros((len(dts),len(DDM[0,:])))

Bq = np.average(DDM[:,-1])
Aqv = []
Bqv = []
for i in range(len(qv)):
	Aq = np.average(DDM[-pointsPerDecade:,i] - Bq)
	Plateau = np.average(DDM[-pointsPerDecade:,i])
	Aqv.append(Aq)
	Bqv.append(Plateau-Aq)
	t_resc[:,i] = dts*qv[i]**2
    #dataw  = np.vstack((dts*qv[i]**2,(DDM[:,i]-Bq)/Aq))
	#print(i, "--- %s seconds ---" % (time.time() - start_time))
	dataw1 = np.vstack((dts*qv[i]**2,(Plateau - DDM[:,i])/Aq))
	dataw2 = np.vstack((dts*qv[i]**2,(Plateau - DDM[:,i])))
#	np.savetxt(outpath+'DDM_Nanoparticles_tresc_s1_axNc'+str(maxNCouples)+'_q'+str(qv[i])+'.dat',dataw.T)
#	np.savetxt(outpath+'DDM_Nanoparticles_tresc_s2_MaxNc'+str(maxNCouples)+'_q'+str(qv[i])+'.dat',dataw1.T)
	np.savetxt(outpath+'DDM_Nanoparticles_tresc_s3_MaxNc'+str(maxNCouples)+'_q'+str(qv[i])+'.dat',dataw2.T)
print("--- %s seconds ---" % (time.time() - start_time))
#print (Bq)
np.savetxt(outpath+'Aq_MaxNc'+str(maxNCouples)+'.dat',np.vstack((qv,Aqv)).T)
np.savetxt(outpath+'Bq_MaxNc'+str(maxNCouples)+'.dat',np.vstack((qv,Bqv)).T)

#print (DDM.shape, len(dts))

dtsw = dts.reshape(1,len(dts))
data = np.concatenate((dtsw.T, DDM), axis=1)
np.savetxt(outpath+'DDM_Nanoparticles_MaxNc'+str(maxNCouples)+'.dat',data)

#sys.exit()



print ("before-save")

vm = 5.7e+10
plt.figure(figsize=(12,12))
# Raw data
subplot(3,3,1).imshow(stack[0], 'gray')
subplot(3,3,2).imshow(stack[-1], 'gray')
subplot(3,3,3).imshow(stack[-1]-stack[0].astype(float), 'gray')
# Differences
subplot(3,3,4).imshow(np.fft.fftshift(spectrumDiff(stack[0], stack[4])),   'hot',vmin=0, vmax=vm)
subplot(3,3,5).imshow(np.fft.fftshift(spectrumDiff(stack[0], stack[200])), 'hot',vmin=0, vmax=vm)
subplot(3,3,6).imshow(np.fft.fftshift(spectrumDiff(stack[0], stack[400])), 'hot',vmin=0, vmax=vm)
# Average of differences
vm = 100.
subplot(3,3,7).imshow(np.fft.fftshift(timeAveraged(stack, 4)),   'hot',vmin=0, vmax=vm)
subplot(3,3,8).imshow(np.fft.fftshift(timeAveraged(stack, 200)), 'hot',vmin=0, vmax=vm)
subplot(3,3,9).imshow(np.fft.fftshift(timeAveraged(stack, 400)), 'hot',vmin=0, vmax=vm)
#
print ("after-save")
plt.savefig(outpath+'FFTfig.png')
plt.show()
print("--- %s seconds ---" % (time.time() - start_time))
