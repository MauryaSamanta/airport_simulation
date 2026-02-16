from Airport.airport_world import AirportWorld
from Aircraft.aircraft import Aircraft
from Aircraft.aircraft_physics import AircraftPhysics
from atc_agents.atc_controller import ATCController


def main():

    # -----------------------
    # Build Airport
    # -----------------------
    world = AirportWorld()
    world.build_airport()

    # -----------------------
    # Create Aircraft
    # -----------------------
    holding_node = world.get_node("Hold_short_17R")

    aircraft1 = Aircraft(
        callsign="AI101",
        current_node=holding_node,
        current_state="WAITING_CLEARANCE"
    )

    aircraft_list = [aircraft1]

    # -----------------------
    # Create ATC
    # -----------------------
    atc = ATCController(world)

    # -----------------------
    # Simulation Loop
    # -----------------------
    dt = 1  # seconds per tick

    for tick in range(100):

        print(f"\nTICK {tick}")

        # 1️⃣ ATC evaluates
        atc.evaluate(aircraft_list)

        # 2️⃣ Update aircraft physics
        for aircraft in aircraft_list:
            AircraftPhysics.update(aircraft, dt)

            # DEBUG PRINT
            print(
                aircraft.callsign,
                aircraft.current_state,
                aircraft.current_node.name if aircraft.current_node else "On Edge",
                aircraft.distance_on_edge,
                aircraft.current_edge.occupied_by if aircraft.current_edge else "No Edge"
            )


if __name__ == "__main__":
    main()
