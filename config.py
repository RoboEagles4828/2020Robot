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
    SHOOTER_SPEED = 0.8
    CLIMBER_SPEED = 0.25
    WINCH_SPEED = 1


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


class Shooter:
    CONVEYOR_SPEED = 1


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
        CLIMBER_0 = 13
        CLIMBER_1 = 16
        WINCH_0_0 = 14
        WINCH_0_1 = 15
        WINCH_1_0 = 17
        WINCH_1_1 = 18


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


class DriveTrain:
    ENCODER_RATIO = 0
