import json

from safety_processes.crevice_safety_process import CreviceSafetyProcess
from safety_processes.dust_storm_safety_process import DustStormSafetyProcess
from safety_processes.rough_terrain_safety_process import RoughTerrainSafetyProcess
from solvers import safety_process_solver



def main():
    safety_process = CreviceSafetyProcess()
    print(json.dumps(safety_process_solver.solve(safety_process, 0.99, 0.001), indent=4))

    safety_process = DustStormSafetyProcess()
    print(json.dumps(safety_process_solver.solve(safety_process, 0.99, 0.001), indent=4))

    safety_process = RoughTerrainSafetyProcess()
    print(json.dumps(safety_process_solver.solve(safety_process, 0.99, 0.001), indent=4))


if __name__ == '__main__':
    main()
