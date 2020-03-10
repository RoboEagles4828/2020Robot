class Robot:
    JOYSTICK_X_MAP_A = 0.75
    JOYSTICK_Y_MAP_A = 0.75
    JOYSTICK_TWIST_MAP_A = 0.5
    JOYSTICK_DEADZONE = 0.05
    JOYSTICK_AVERAGE_PERIOD = 0
    CAMERA_YAW_POS_0 = 0.19
    CAMERA_YAW_POS_1 = 0.90

    class Drivetrain:
        DRIVE_SPEED = 0.35
        DRIVE_SLOW_SPEED = 0.2
        DRIVE_TURN_SPEED = 0.3
        VISION_RATIO = 0.5
        VISION_MIN_SPEED = 0.13
        VISION_CUTOFF = 0.02

    class Shooter:
        INTAKE_SPEED = 0.5
        OUTTAKE_SPEED = 0.5
        INTAKE_CONTROL_SPEED = 0.6
        CONVEYOR_SPEED = 0.5
        SHOOTER_SPEED_0 = 0.77
        SHOOTER_SPEED_1 = 0.95

    class Climber:
        CLIMBER_LEFT_UP_SPEED = 0.60
        CLIMBER_RIGHT_UP_SPEED = 0.45
        WINCH_LEFT_FRONT_UP_SPEED = 1.0
        WINCH_LEFT_BACK_UP_SPEED = 1.0
        WINCH_RIGHT_FRONT_UP_SPEED = 1.0
        WINCH_RIGHT_BACK_UP_SPEED = 1.0
        CLIMBER_LEFT_DOWN_SPEED = 0.60
        CLIMBER_RIGHT_DOWN_SPEED = 0.60
        WINCH_LEFT_FRONT_DOWN_SPEED = 1.0
        WINCH_LEFT_BACK_DOWN_SPEED = 1.0
        WINCH_RIGHT_FRONT_DOWN_SPEED = 1.0
        WINCH_RIGHT_BACK_DOWN_SPEED = 1.0

    class ShooterController:
        SHOOTER_VELOCITY_0 = 1.93
        SHOOTER_VELOCITY_1 = 2.10
        SHOOTER_VELOCITY_2 = 2.40


class Ports:

    CAMERA_SERVO_YAW = 1

    class Drivetrain:
        LEFT_0 = 1
        LEFT_1 = 2
        RIGHT_0 = 3
        RIGHT_1 = 4

    class Shooter:
        INTAKE = 5
        CONVEYOR = 7
        CONVEYOR_PROX_FRONT_0 = 7
        CONVEYOR_PROX_FRONT_1 = 8
        CONVEYOR_PROX_BACK = 9
        SHOOTER_LEFT = 11
        SHOOTER_RIGHT = 12
        SHOOTER_PISTON_0 = 5
        SHOOTER_PISTON_1 = 7

    class Climber:
        CLIMBER_LEFT = 16
        CLIMBER_RIGHT = 13
        WINCH_LEFT_FRONT = 18
        WINCH_LEFT_BACK = 17
        WINCH_RIGHT_FRONT = 14
        WINCH_RIGHT_BACK = 15


class Buttons:
    class Joystick0:
        CAMERA = 11

        class Drivetrain:
            VISION = 1

        class Shooter:
            CONVEYOR = 7

    class Joystick1:
        class Climber:
            WINCH_LEFT_FRONT = 9
            WINCH_LEFT_BACK = 11
            WINCH_RIGHT_FRONT = 10
            WINCH_RIGHT_BACK = 12
            LEFT_UP = 5
            LEFT_DOWN = 3
            RIGHT_UP = 6
            RIGHT_DOWN = 4

        class Shooter:
            INTAKE = 1
            OUTTAKE = 2
            SHOOT_0 = 7
            SHOOT_1 = 8


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
    DS_8_TURN = 67.5
    DS_8_FORWARD_MID = 86.3
    DS_8_BACK_MID = 68.3
    DS_SHOOT = 178.0


class Drivetrain:
    ENCODER_RATIO = 1 / 1460


class Shooter:
    CONVEYOR_INTAKE_SPEED = 0.40
    CONVEYOR_SHOOT_SPEED = 0.65


class ShooterController:
    P_LEFT = 0.0
    I_LEFT = 0.0
    D_LEFT = 0.0
    F_LEFT = 0.25
    P_RIGHT = 0.0
    I_RIGHT = 0.0
    D_RIGHT = 0.0
    F_RIGHT = 0.25
