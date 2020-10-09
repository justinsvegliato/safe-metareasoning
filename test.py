import json

from mlc.wheel_motor_temperature_mlc import WheelMotorTemperatureMlc
from mlc.arm_motor_temperature_mlc import ArmMotorTemperatureMlc
from mlc.obstacle_mlc import ObstacleMlc
from solvers import mlc_solver
from printers import mlc_printer

def main():
    mlc = WheelMotorTemperatureMlc()
    print(json.dumps(mlc_solver.solve(mlc, 0.99, 0.001), indent=4))

    # mlc = ArmMotorTemperatureMlc()
    # print(json.dumps(mlc_solver.solve(mlc, 0.99, 0.001), indent=4))

    # mlc = ObstacleMlc()
    # print(json.dumps(mlc_solver.solve(mlc, 0.99, 0.001), indent=4))


if __name__ == '__main__':
    main()
