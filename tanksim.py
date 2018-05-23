import math
# Importerer moduler for eulers metode og animasjon med PyGame
from moduler import euler
from moduler import animasjon

def getSurfaceArea(tank_params, h):
    ''' Finner overflateareal ved gitt høyde for konisk tank.
        Inn-parametere er radius i bunn (R2), 
        differansen i radius oppe og nede (R1), 
        starthøyden (h_0) og høyden (h)'''
    return math.pi*(tank_params["R2"] + tank_params["R1"] / tank_params["max_height"] * h)**2

# Definerer tanker med variablene deres
# Liten konisk metallbøtte
tank1_params = {
    "max_height": 9, # Bøttas maksimale høyde
    "h_0": 9,    # Starthøyde gitt i cm
    "R1": 2.35,  # Avvik fra konstant radius
    "R2": 4.55,  # Konstant radius
    "h_1": 1.5,  # Simuleringsstopp gitt i cm over hullet
    "C": 0.6783407237648454,  # Korreksjonsfaktor for vann gjennom hull (denne er eksakt)
    "A_hull": math.pi*(0.2/2)**2 # Areal av hull
}
# Finner overflateareal ved h_0
tank1_params["areal"] = getSurfaceArea(tank1_params, tank1_params["h_0"])
# Definerer tanken som en klasse for eulers metode
tank1 = euler.Tank(tank1_params["A_hull"], tank1_params["areal"], tank1_params["h_0"], tank1_params["C"])

# Stor konisk metallbøtte
tank2_params = {
    "max_height": 12, # Bøttas maksimale høyde
    "h_0": 12,   # Starthøyde gitt i cm
    "R1": 2.35,  # Avvik fra konstant radius
    "R2": 5.95,  # Konstant radius
    "h_1": 1.2,  # Simuleringsstopp gitt i cm over hullet
    "C": 0.73,   # Korreksjonsfaktor for vann gjennom hull
    "A_hull": math.pi*(0.3/2)**2 # Areal av hull
}
# Finner overflateareal ved h_0
tank2_params["areal"] = getSurfaceArea(tank2_params, tank2_params["h_0"])
# Definerer tanken som en klasse for eulers metode
tank2 = euler.Tank(tank2_params["A_hull"], tank2_params["areal"], tank2_params["h_0"], tank2_params["C"])

# Rektangulær tank
tank3_params = {
    "max_height": 15, # Bøttas maksimale høyde
    "h_0": 15,       # Starthøyde gitt i cm
    "lengde": 19.5,  # Lengde i cm
    "bredde": 28,    # Bredde i cm
    "h_1": 2,      # Simuleringsstopp gitt i cm over hullet
    "C": 0.61,      # Korreksjonsfaktor for vann gjennom hull
    "A_hull": math.pi*(0.4/2)**2 # Areal av hull
}
# Finner overflateareal ved h_0
tank3_params["areal"] = tank3_params["lengde"] * tank3_params["bredde"]
# Definerer tanken som en klasse for eulers metode
tank3 = euler.Tank(tank3_params["A_hull"], tank3_params["areal"], tank3_params["h_0"], tank3_params["C"])

# Blå konisk plastbøtte
tank4_params = {
    "max_height": 21, # Bøttas maksimale høyde
    "h_0": 2,   # Starthøyde gitt i cm
    "R1": 2.75,  # Avvik fra konstant radius
    "R2": 9.5,   # Konstant radius
    "h_1": 2,    # Simuleringsstopp gitt i cm over hullet
    "C": 0.52,   # Korreksjonsfaktor for vann gjennom hull
    "A_hull": math.pi*(0.5/2)**2 # Areal av hull
}
# Finner overflateareal ved h_0
tank4_params["areal"] = getSurfaceArea(tank4_params, tank4_params["h_0"])
# Definerer tanken som en klasse for eulers metode
tank4 = euler.Tank(tank4_params["A_hull"], tank4_params["areal"], tank4_params["h_0"], tank4_params["C"])

DELTA_T = euler.DELTA_T
print(DELTA_T)
# Finner antall desimaler for DELTA_T, denne trengs senere
if type(DELTA_T) is int:
    rnd = 0
else:
    rnd = str(DELTA_T)[::-1].find('.')

levels = [{0:tank1_params["h_0"]},{0:tank2_params["h_0"]},{0:tank3_params["h_0"]},{0:tank4_params["h_0"]}] # Plassholder for høyden gitt tiden
run = True # Bestemmer om simuleringen forsatt skal kjøre
time = 0 # Tiden i sekunder
q_inn = 0 # cm^3/s inn i øverste tank (tank1)

# Kjører simuleringen og samler data
while run:
    if tank1.fluidHeight > tank1_params["h_1"]:
        tank1_params["areal"] = getSurfaceArea(tank1_params, list(levels[0].values())[-1])
        tank1.AREA_SURFACE = tank1_params["areal"]
        tank1.runStep(q_inn)
        levels[0][round(time,rnd)] = tank1.fluidHeight
        q_ut_tank1 = tank1_params["A_hull"] * tank1.getFlowVelocity(list(levels[0].values())[-1])
    elif q_ut_tank1 != 0: #time == len(list(levels[0].values())):
        print("Tank1 tom etter {}s = {}min".format(round(time,2), round(time/60,2)))
        q_ut_tank1 = 0

    if tank2.fluidHeight > tank2_params["h_1"]:
        tank2_params["areal"] = getSurfaceArea(tank2_params, list(levels[1].values())[-1])
        tank2.AREA_SURFACE = tank2_params["areal"]
        tank2.runStep(q_ut_tank1)
        levels[1][round(time,rnd)] = tank2.fluidHeight
        q_ut_tank2 = tank2_params["A_hull"] * tank2.getFlowVelocity(list(levels[1].values())[-1])
    elif q_ut_tank2 != 0: #time == len(list(levels[1].values())):
        print("Tank2 tom etter {}s = {}min".format(round(time,2), round(time/60,2)))
        q_ut_tank2 = 0

    if tank3.fluidHeight > tank3_params["h_1"]:
        tank3.AREA_SURFACE = tank3_params["areal"]
        tank3.runStep(q_ut_tank2)
        levels[2][round(time,rnd)] = tank3.fluidHeight
        q_ut_tank3 = tank3_params["A_hull"] * tank3.getFlowVelocity(list(levels[2].values())[-1])
    elif q_ut_tank3 != 0: #time == len(list(levels[2].values())):
        print("Tank3 tom etter {}s = {}min".format(round(time,2), round(time/60,2)))
        q_ut_tank3 = 0

    if tank4.fluidHeight > tank4_params["h_1"] or time == 0:
        tank4_params["areal"] = getSurfaceArea(tank4_params, list(levels[3].values())[-1])
        tank4.AREA_SURFACE = tank4_params["areal"]
        tank4.runStep(q_ut_tank3)
        levels[3][round(time,rnd)] = tank4.fluidHeight
    else:
        print("Tank4 tom etter {}s = {}min".format(round(time,2), round(time/60,2)))
        run = False # Simuleringen er ferdig
    time += DELTA_T

# Importerer matplotlib og plotter simuleringen
import matplotlib.pyplot as plt
for index, fluidHeights in enumerate(levels):
    plt.plot(list(fluidHeights.keys()), list(fluidHeights.values()), label="Tank {}".format(index+1))

# Plotter målinger
measurements = [
    {0:9,47:8,99:7,149:6,203:5,259:4,304:3,367:2},                                                              # Målinger for tank 1
    {79:10,129:9,171:8,213:7,253:6,302:5,346:4,394:3},                                                          # Målinger for tank 2
    {104:14,191:13,280:12,353:11,459:9.5,493:9,574:7.5,616:7,674:6,754:4.8,816:4,904:3,1017:2},                 # Målinger for tank 3
    {37:2.5,95:3.5,180:4.5,277:5.1,331:5.5,535:5.6,593:5.4,652:5.2,716:4.9,768:4.5,843:4,905:3.5,955:3,1053:2}  # Målinger for tank 4
]
colors = ["C1","g","r","b"]
for  index, mm in enumerate(measurements):
    plt.plot(list(mm.keys()), list(mm.values()), "{}s".format(colors[index]), label="Målinger for tank {}".format(index+1))

# Legger til detaljer og viser plot
plt.title("Tanksimulering av 4 tanker")
plt.ylabel('Høyde [cm]')
plt.xlabel('Tid [s]')
plt.legend()
plt.grid()
plt.show()

# Starter animasjon
animasjon.animate(levels[0],levels[1],levels[2],levels[3],[tank1_params,tank2_params,tank3_params,tank4_params],DELTA_T,rnd)
