class Robot:
    JOYSTICK_X_MAP_A = 0.5
    JOYSTICK_Y_MAP_A = 0.5
    JOYSTICK_TWIST_MAP_A = 0.25
    JOYSTICK_DEADZONE = 0.05
    JOYSTICK_AVERAGE_PERIOD = 0
    DRIVE_SPEED = 0.7
    DRIVE_SLOW_SPEED = 0.3
    DRIVE_TURN_SPEED = 0.7
    INTAKE_SPEED = 1.0
    CONVEYOR_SPEED = 1.0
    SHOOTER_SPEED = 0.8


class Ports:
    class Drivetrain:
        LEFT_0 = 1
        LEFT_1 = 2
        RIGHT_0 = 3
        RIGHT_1 = 4

    class Shooter:
        INTAKE = 5
        INTAKE_PISTON = 6
        CONVEYOR = 7
        CONVEYOR_PROX_FRONT = 8
        CONVEYOR_PROX_BACK = 9
        SHOOTER_LEFT = 10
        SHOOTER_RIGHT = 11
        SHOOTER_PISTON_0 = 12
        SHOOTER_PISTON_1 = 13


class Buttons:
    class Shooter:
        INTAKE = 2
        SHOOTER = 1


class DriveTrain:
    ENCODER_RATIO = 0
