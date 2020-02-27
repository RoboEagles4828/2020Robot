class Robot:
    JOYSTICK_X_MAP_A = 0.5
    JOYSTICK_Y_MAP_A = 0.5
    JOYSTICK_TWIST_MAP_A = 0.25
    JOYSTICK_DEADZONE = 0.05
    JOYSTICK_AVERAGE_PERIOD = 0
    DRIVE_SPEED = 0.7
    DRIVE_SLOW_SPEED = 0.3
    DRIVE_TURN_SPEED = 0.7
    VISION_RATIO = 0.5
    INTAKE_SPEED = 0.6
    SHOOTER_SPEED_10 = 0.83
    SHOOTER_SPEED_20 = 0.95
    CLIMBER_UP_SPEED = 0.31
    CLIMBER_DOWN_SPEED = 0.15
    WINCH_UP_SPEED = 1.0
    WINCH_DOWN_SPEED = 1.0


class Autonomous:
    POS_1_FORWARD = 43.3
    POS_1_TO_TRENCH = 66.9
    POS_1_TRENCH = 156.3
    POS_2_TRENCH_TURN = 17.9
    POS_2_TURN = 29.1
    POS_2_TO_TRENCH = 86.6
    POS_2_TRENCH = 108
    POS_3_SHOOT = 134.9
    POS_3_TURN = 60.9
    POS_3_TRENCH = 130.4
    DRIVE_DISTANCE = 50.0
    DS_8_TO_MID = 60.0
    DS_8_TURN = 22.5
    DS_8_FORWARD_MID = 86.3
    DS_8_BACK_MID = 68.3
    DS_SHOOT = 178.0


class Drivetrain:
    ENCODER_RATIO = 1 / 1460


class Shooter:
    CONVEYOR_SPEED = 0.85


class Ports:

    CAMERA_SERVO_YAW = 1
    CAMERA_SERVO_PITCH = 0

    class Drivetrain:
        LEFT_0 = 1
        LEFT_1 = 2
        RIGHT_0 = 3
        RIGHT_1 = 4

    class Shooter:
        INTAKE = 5
        INTAKE_CONTROL = 6
        CONVEYOR = 7
        CONVEYOR_PROX_FRONT = 8
        CONVEYOR_PROX_BACK = 9
        SHOOTER_LEFT = 11
        SHOOTER_RIGHT = 12
        SHOOTER_PISTON_0 = 5
        SHOOTER_PISTON_1 = 7

    class Climber:
        CLIMBER_0 = 16
        CLIMBER_1 = 13
        WINCH_0_0 = 18
        WINCH_0_1 = 17
        WINCH_1_0 = 15
        WINCH_1_1 = 14


class Buttons:
    class Drivetrain:
        VISION = 9

    class Shooter:
        INTAKE = 2
        OUTTAKE = 12
        SHOOTER = 1

    class Climber:
        UP = 7
        DOWN = 8
        LEFT_UP = 5
        LEFT_DOWN = 3
        RIGHT_UP = 6
        RIGHT_DOWN = 4
