class Robot:
    JOYSTICK_X_MAP_A = 0.5
    JOYSTICK_Y_MAP_A = 0.5
    JOYSTICK_TWIST_MAP_A = 0.25
    JOYSTICK_DEADZONE = 0.05
    JOYSTICK_AVERAGE_PERIOD = 0
    INTAKE_SPEED = 1
    CONVEYOR_SPEED = 1
    SHOOTER_SPEED = 1


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


class Buttons:
    class Shooter:
        INTAKE = 2
        SHOOTER = 1
