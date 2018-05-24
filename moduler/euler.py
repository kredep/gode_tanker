
#units in m or m^2

#not in use
#VELOCITY_COEFFICIENT = 0.51#0.51#0.97
#CONTRACTION_COEFFICIENT = 0.62
#K = VELOCITY_COEFFICIENT*((G*2)**0.5)

G = 981

DELTA_T = 1

class Tank:
    def __init__(self,AA = 1,AS = 1,FH = 1,c=0.61):
            self.AREA_APERTURE = AA
            self.AREA_SURFACE = AS
            self.fluidHeight = FH
            self.K = c*((G*2)**0.5)

    def runStep(self,q_in):
        #remove fluid that runs out of the tank
        self.changeVolume(self.getVolumeDiff()*DELTA_T)
        #add fluid that runs in to the tank
        self.changeVolume(q_in*DELTA_T)

    def getFlowVelocity(self,H):
        return self.K*(H**0.5)

    def getVolumeDiff(self):
        return -self.getFlowVelocity(self.fluidHeight)*self.AREA_APERTURE

    def changeVolume(self,volume):
        self.fluidHeight += volume/self.AREA_SURFACE


if __name__ == '__main__':
    time = 0

    tank = Tank(1,1,1,0.64)

    while tank.fluidHeight > 0.015:
        tank.runStep(0.1)
        time+=1
        print("H= {}, T= {}".format(tank.fluidHeight,time*DELTA_T))
        
