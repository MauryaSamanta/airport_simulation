from Airport.airport_world import AirportWorld
from Aircraft.aircraft import Aircraft
from Aircraft.aircraft_physics import AircraftPhysics

from atc_agents.atc_agent import ATCAgent
from atc_agents.pilot_agent import PilotAgent

from communication.message_bus import MessageBus
from ui import Visualizer

import pygame
import random


def main():

    pygame.init()

    # --------------------------------------------------
    # WORLD
    # --------------------------------------------------
    world = AirportWorld()
    world.build_airport()

    aircraft_list = []

    # --------------------------------------------------
    # COMMUNICATION BUS
    # --------------------------------------------------
    bus = MessageBus()

    # --------------------------------------------------
    # AGENTS
    # --------------------------------------------------
    atc_agent = ATCAgent(bus)

    pilot_agents = []

    # --------------------------------------------------
    # UI
    # --------------------------------------------------
    visualizer = Visualizer(world, aircraft_list)

    # --------------------------------------------------
    # SIMULATION VARIABLES
    # --------------------------------------------------
    running = True
    dt = 0.1

    spawn_interval = 2000  # milliseconds
    last_spawn_time = 0
    aircraft_counter = 100

    gates = ["A1", "A2"]

    # --------------------------------------------------
    # SPAWN FUNCTION
    # --------------------------------------------------
    def spawn_aircraft():
        nonlocal aircraft_counter

        gate_name = random.choice(gates)
        gate_node = world.get_node(gate_name)

        callsign = f"AI{aircraft_counter}"
        aircraft_counter += 1

        new_aircraft = Aircraft(
            callsign=callsign,
            current_node=gate_node,
            current_state="PARKED",
            speed=0.0
        )

        aircraft_list.append(new_aircraft)

        # Create pilot agent
        pilot = PilotAgent(new_aircraft, bus)
        pilot_agents.append(pilot)

    # --------------------------------------------------
    # MAIN LOOP
    # --------------------------------------------------
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_time = pygame.time.get_ticks()

        # Spawn aircraft periodically
        if current_time - last_spawn_time > spawn_interval:
            spawn_aircraft()
            last_spawn_time = current_time

        # --------------------------------------------------
        # AGENT DECISION CYCLE
        # --------------------------------------------------

        # ATC observes world and plans
        atc_agent.plan(world, aircraft_list)
        
        # Pilots observe messages and plan
        for pilot in pilot_agents:
            pilot.plan(world)

        # Execute actions
        atc_agent.act()

        for pilot in pilot_agents:
            pilot.act()

        # --------------------------------------------------
        # PHYSICS UPDATE
        # --------------------------------------------------
        for aircraft in aircraft_list:
            AircraftPhysics.update(aircraft, dt)

        # --------------------------------------------------
        # CLEANUP DEPARTED AIRCRAFT
        # --------------------------------------------------
        for aircraft in aircraft_list[:]:
            if aircraft.current_state == "AIRBORNE":
                if aircraft.current_edge is None:
                    aircraft_list.remove(aircraft)

                    # remove associated pilot agent
                    pilot_agents[:] = [
                        p for p in pilot_agents
                        if p.aircraft != aircraft
                    ]

        # --------------------------------------------------
        # UI UPDATE
        # --------------------------------------------------
        visualizer.update()

    pygame.quit()


if __name__ == "__main__":
    main()