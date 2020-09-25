import os
import sys
import numpy as np
import h5py

class FlowField:
	def __init__(self, filename_in):
		self.filename = filename_in
		self.mainObj = h5py.File(self.filename, 'r')
		self.numLevels = 0
		self.is3d = False
		while ('level_{}'.format(self.numLevels) in self.mainObj.keys()):
		    self.numLevels = self.numLevels + 1
		self.ChomboGlobal = self.mainObj['Chombo_global']
		self.levels = []
		self.boxes = []
		self.numBoxes = []
		self.dataDescriptors = []
		self.attr = []
		self.dsizes = []
		self.dtypes = []
		self.data = []
		self.totalBlocks = 0
		self.lnblocks = 0
		for i in range(self.numLevels):
			lvl = self.mainObj['level_{}'.format(i)]
			self.levels.append(i)
			bx = lvl['boxes']
			self.boxes.append(bx[...]) #i low, j low, i high, j high, ()
			self.numBoxes.append(bx.shape[0])
			self.totalBlocks = self.totalBlocks + self.numBoxes[i]
			self.dataDescriptors.append(lvl['data:datatype=0'])
			self.attr.append(lvl['data_attributes'])
			self.dsizes.append(self.dataDescriptors[i].shape[0])
			self.data.append(self.dataDescriptors[i][...])
		self.is3d = len(self.boxes[0][0])==6
		self.lnblocks = self.totalBlocks
		self.nxb = 0
		self.nyb = 0
		self.nzb = 0
		self.blockSize = []
		if (self.is3d):
			self.nxb = self.boxes[0][0][3] - self.boxes[0][0][0] + 1
			self.nyb = self.boxes[0][0][4] - self.boxes[0][0][1] + 1
			self.nzb = self.boxes[0][0][5] - self.boxes[0][0][2] + 1
		else:
			self.nxb = self.boxes[0][0][2] - self.boxes[0][0][0] + 1
			self.nyb = self.boxes[0][0][3] - self.boxes[0][0][1] + 1
			self.nzb = 1
		self.blockSize.append(self.nxb)
		self.blockSize.append(self.nyb)
		if self.is3d:
			self.blockSize.append(self.nzb)
			
	def Flow(self, n1, i1, j1, k1, lb1):
		nguardOut = 2
		n = n1+2
		i = i1-1-nguardOut
		j = j1-1-nguardOut
		k = k1-1-nguardOut
		nx = self.nxb + 2*nguardOut
		ny = self.nxb + 2*nguardOut
		nz = self.nxb + 2*nguardOut
		if (not self.is3d):
			k = 0
			nz = 1
		lb = lb1-1
		levelIndex = 0
		lbacc = 0
		totallb = self.numBoxes[0]
		while (lb >= totallb):
			lbacc = lbacc + self.numBoxes[levelIndex]
			levelIndex = levelIndex	+ 1
			totallb = self.numBoxes[levelIndex]
		lbeff = lb - lbacc
		lnblocksLevel = self.numBoxes[levelIndex]
		data = self.data[levelIndex]
		nvars = 7
		if (self.is3d):
			nvars = 8
		idx = n + i*nvars + j*nvars*nx + k*nvars*nx*ny + lbeff*nvars*nx*ny*nz
		idx = i + j*nx + k*nx*ny + n*nx*ny*nz + lbeff*nx*ny*nz*nvars
		#print(nx*ny*nz*lnblocksLevel*nvars)
		#print(len(data))
		#print("{}, {}, {}, {}, {}".format(nx, ny, nz, nvars, lnblocksLevel))
		#np.savetxt("foo.csv", data, delimiter=",")
		return data[idx]
		
	def __str__(self):
		output = ''
		output = output + "3D: {}\n".format(self.is3d)
		output = output + "Levels: {}\n".format(self.numLevels)
		output = output + "Block Size: {}\n".format(self.blockSize)
		output = output + "Block Count: {}\n".format(self.totalBlocks)
		return output
		