class BuildingAlarm:
    def turn_on(self):
        print("Building alarm: ON")

    def turn_off(self):
        print("Building alarm: OFF")


class LegacyElevatorSystem:
    def engage_fire_service(self):
        print("Elevators: EMERGENCY MODE")

    def resume_standard_service(self):
        print("Elevators: NORMAL MODE")


class IndustrialVentilationUnit:
    def halt_airflow(self):
        print("Ventilation: OFF")

    def resume_airflow(self):
        print("Ventilation: ON")


class SecurityDoorController:
    def release_all_exits(self):
        print("Emergency doors: UNLOCKED")

    def secure_all_exits(self):
        print("Emergency doors: LOCKED")


class FireSuppressionController:
    def begin_water_suppression(self):
        print("Sprinklers: ON")

    def end_water_suppression(self):
        print("Sprinklers: OFF")


class SmokeSensor:
    def __init__(self, alarm, elevator, ventilation, doors):
        self.alarm = alarm
        self.elevator = elevator
        self.ventilation = ventilation
        self.doors = doors

    def detect_smoke(self):
        print("\n=== SMOKE DETECTED ===")
        print("Smoke sensor: smoke detected")
        self.alarm.turn_on()
        self.ventilation.halt_airflow()
        self.elevator.engage_fire_service()
        self.doors.release_all_exits()


class FireSensor:
    def __init__(self, alarm, elevator, ventilation, doors, sprinklers):
        self.alarm = alarm
        self.elevator = elevator
        self.ventilation = ventilation
        self.doors = doors
        self.sprinklers = sprinklers

    def confirm_fire(self):
        print("\n=== FIRE CONFIRMED ===")
        print("Fire sensor: fire confirmed")
        self.alarm.turn_on()
        self.ventilation.halt_airflow()
        self.elevator.engage_fire_service()
        self.doors.release_all_exits()
        self.sprinklers.begin_water_suppression()


class EmergencyPanel:
    def __init__(self, alarm, elevator, ventilation, doors, sprinklers):
        self.alarm = alarm
        self.elevator = elevator
        self.ventilation = ventilation
        self.doors = doors
        self.sprinklers = sprinklers

    def clear_emergency(self):
        print("\n=== EMERGENCY CLEARED ===")
        print("Emergency panel: returning building to normal")
        self.alarm.turn_off()
        self.sprinklers.end_water_suppression()
        self.ventilation.resume_airflow()
        self.elevator.resume_standard_service()
        self.doors.secure_all_exits()


if __name__ == "__main__":
    alarm = BuildingAlarm()
    elevator = LegacyElevatorSystem()
    ventilation = IndustrialVentilationUnit()
    doors = SecurityDoorController()
    sprinklers = FireSuppressionController()

    smoke_sensor = SmokeSensor(
        alarm,
        elevator,
        ventilation,
        doors
    )

    fire_sensor = FireSensor(
        alarm,
        elevator,
        ventilation,
        doors,
        sprinklers
    )

    emergency_panel = EmergencyPanel(
        alarm,
        elevator,
        ventilation,
        doors,
        sprinklers
    )

    smoke_sensor.detect_smoke()
    fire_sensor.confirm_fire()
    emergency_panel.clear_emergency()
