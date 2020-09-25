import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../py'))
import ChampsData

basedir = os.path.join(os.path.dirname(os.path.realpath(__file__)))
file3d = ChampsData.FlowField(os.path.join(basedir, 'files/3d.hdf5'))
filevort = ChampsData.FlowField(os.path.join(basedir, 'files/iv1k.hdf5'))
filevortinfo = ChampsData.FlowField(os.path.join(basedir, 'files/ivinfo.hdf5'))
filemulti2d = ChampsData.FlowField(os.path.join(basedir, 'files/multilevel2d.hdf5'))

#print(file3d)
print(filevort)
print(filevort.Flow(1, 36, 36, 36, 16))
print(filevort.Flow(2, 36, 36, 36, 16))
print(filevort.Flow(3, 36, 36, 36, 16))
print(filevort.Flow(4, 36, 36, 36, 16))

#print(filevortinfo)
#print(filemulti2d)
sys.exit(1)