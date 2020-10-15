import json

from mlc.arm_motor_temperature_mlc import ArmMotorTemperatureMlc
from mlc.crevice_mlc import CreviceMlc
from mlc.dust_storm_mlc import DustStormMlc
from mlc.wheel_motor_temperature_mlc import WheelMotorTemperatureMlc
from printers import mlc_printer
from solvers import mlc_solver


def main():
    # mlc = ArmMotorTemperatureMlc()
    # print(json.dumps(mlc_solver.solve(mlc, 0.99, 0.001), indent=4))

    # mlc = CreviceMlc()
    # print(json.dumps(mlc_solver.solve(mlc, 0.99, 0.001), indent=4))

    mlc = DustStormMlc()
    print(json.dumps(mlc_solver.solve(mlc, 0.99, 0.001), indent=4))

    # mlc = WheelMotorTemperatureMlc()
    # print(json.dumps(mlc_solver.solve(mlc, 0.99, 0.001), indent=4))


if __name__ == '__main__':
    main()
