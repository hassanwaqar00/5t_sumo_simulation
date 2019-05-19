
from __future__ import absolute_import
from __future__ import print_function
import math
import optparse
import os
import random
import sys
import traci
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..',
                                 '..', '..', '..', "tools"))  # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary
except ImportError:
    sys.exit("please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")


def run():
    step = 0
    locationSamplingPeriod = 1
    print('Starting simulation at step=' + repr(step))
    dump = open('simulation_output_dump.csv', 'w')
    print('step,id,speed,positionX,positionY,angle', file=dump)
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        if step % locationSamplingPeriod == 0:
            if step % (30 * 60) == 0:
                print(step / 60 / 60)
            for id in traci.vehicle.getIDList():
                if traci.vehicle.getTypeID(id) == 'carVIL':  # car with VIL
                    print('%d,%s,%.2f,%.2f,%.2f,%.2f' %
                          (step, id, traci.vehicle.getSpeed(id)*3.6,
                           traci.vehicle.getPosition(id)[0],
                           traci.vehicle.getPosition(id)[1],
                           traci.vehicle.getAngle(id)),
                          file=dump)
        step += 1
    print('Completed simulation at step=' + repr(step))
    traci.close()
    sys.stdout.flush()


if __name__ == '__main__':
    sumoBinary = checkBinary('sumo')
    traci.start([sumoBinary, '-c', 'config.sumocfg',
                 '--tripinfo-output', 'trip_info_output.xml'])
    run()
