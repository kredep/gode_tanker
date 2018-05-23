
#units in m or m^2

#not in use
#VELOCITY_COEFFICIENT = 0.51#0.51#0.97
#CONTRACTION_COEFFICIENT = 0.62
#K = VELOCITY_COEFFICIENT*((G*2)**0.5)

G = 981

DELTA_T = 1

class Tank:
    def __init__(self,AA = 1,AS = 1,FH = 1,c=0.61):
            self.AREA_APERTURE = AA #0.00001
            self.AREA_SURFACE = AS #0.196*0.28
            self.fluidHeight = FH #0.021
            self.K = c*((G*2)**0.5)

    def runStep(self,q_in):
        self.fluidHeight -=(self.getHeightDiff(
            self.fluidHeight,
            self.AREA_APERTURE,
            self.AREA_SURFACE)*DELTA_T
            - (q_in/self.AREA_SURFACE)*DELTA_T)

    def getFlowVelocity(self,H):
        return self.K*(H**0.5)

    def getHeightDiff(self,H,AA,AS):
        return self.getFlowVelocity(H)*(AA/AS)#*CONTRACTION_COEFFICIENT


if __name__ == '__main__':
    time = 0

    tank = Tank(1,1,1,0.64)

    while tank.fluidHeight > 0.015:
        tank.runStep(0.1)
        time+=1
        print("H= {}, T= {}".format(tank.fluidHeight,time*DELTA_T))
        
