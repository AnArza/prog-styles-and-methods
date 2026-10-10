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


class ElevatorAdapter:
    def __init__(self, elevator_system):
        self.elevator_system = elevator_system

    def enter_emergency_mode(self):
        self.elevator_system.engage_fire_service()

    def return_to_normal(self):
        self.elevator_system.resume_standard_service()


class VentilationAdapter:
    def __init__(self, ventilation_unit):
        self.ventilation_unit = ventilation_unit

    def turn_off(self):
        self.ventilation_unit.halt_airflow()

    def turn_on(self):
        self.ventilation_unit.resume_airflow()


class EmergencyDoorAdapter:
    def __init__(self, door_controller):
        self.door_controller = door_controller

    def unlock(self):
        self.door_controller.release_all_exits()

    def lock(self):
        self.door_controller.secure_all_exits()


class SprinklerAdapter:
    def __init__(self, sprinkler_controller):
        self.sprinkler_controller = sprinkler_controller

    def activate(self):
        self.sprinkler_controller.begin_water_suppression()

    def deactivate(self):
        self.sprinkler_controller.end_water_suppression()


class SmokeSensor:
    def __init__(self, mediator=None):
        self.mediator = mediator

    def detect_smoke(self):
        print("\n=== SMOKE DETECTED ===")
        print("Smoke sensor: smoke detected")

        if self.mediator:
            self.mediator.notify(self, "smoke_detected")


class FireSensor:
    def __init__(self, mediator=None):
        self.mediator = mediator

    def confirm_fire(self):
        print("\n=== FIRE CONFIRMED ===")
        print("Fire sensor: fire confirmed")

        if self.mediator:
            self.mediator.notify(self, "fire_confirmed")


class EmergencyPanel:
    def __init__(self, mediator=None):
        self.mediator = mediator

    def clear_emergency(self):
        print("\n=== EMERGENCY CLEARED ===")
        print("Emergency panel: returning building to normal")

        if self.mediator:
            self.mediator.notify(self, "emergency_cleared")


class EmergencyMediator:
    def __init__(
        self,
        alarm,
        elevator,
        ventilation,
        doors,
        sprinklers,
        smoke_sensor,
        fire_sensor,
        emergency_panel
    ):
        self.alarm = alarm
        self.elevator = elevator
        self.ventilation = ventilation
        self.doors = doors
        self.sprinklers = sprinklers

        self.smoke_sensor = smoke_sensor
        self.fire_sensor = fire_sensor
        self.emergency_panel = emergency_panel

        self.smoke_sensor.mediator = self
        self.fire_sensor.mediator = self
        self.emergency_panel.mediator = self

    def notify(self, sender, event):
        if event == "smoke_detected":
            print("Mediator: activating smoke emergency response")
            self.alarm.turn_on()
            self.ventilation.turn_off()
            self.elevator.enter_emergency_mode()
            self.doors.unlock()

        elif event == "fire_confirmed":
            print("Mediator: escalating to confirmed fire response")
            self.alarm.turn_on()
            self.ventilation.turn_off()
            self.elevator.enter_emergency_mode()
            self.doors.unlock()
            self.sprinklers.activate()

        elif event == "emergency_cleared":
            print("Mediator: restoring normal building operation")
            self.alarm.turn_off()
            self.sprinklers.deactivate()
            self.ventilation.turn_on()
            self.elevator.return_to_normal()
            self.doors.lock()


if __name__ == "__main__":
    alarm = BuildingAlarm()

    legacy_elevator = LegacyElevatorSystem()
    industrial_ventilation = IndustrialVentilationUnit()
    security_doors = SecurityDoorController()
    fire_suppression = FireSuppressionController()

    elevator = ElevatorAdapter(legacy_elevator)
    ventilation = VentilationAdapter(industrial_ventilation)
    doors = EmergencyDoorAdapter(security_doors)
    sprinklers = SprinklerAdapter(fire_suppression)

    smoke_sensor = SmokeSensor()
    fire_sensor = FireSensor()
    emergency_panel = EmergencyPanel()

    mediator = EmergencyMediator(
        alarm,
        elevator,
        ventilation,
        doors,
        sprinklers,
        smoke_sensor,
        fire_sensor,
        emergency_panel
    )

    smoke_sensor.detect_smoke()
    fire_sensor.confirm_fire()
    emergency_panel.clear_emergency()
