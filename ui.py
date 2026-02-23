import pygame
import math


class Visualizer:

    def __init__(self, world, aircraft_list, bus):

        pygame.init()

        self.width = 1200
        self.height = 700

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("ATC Radar Display")

        self.world = world
        self.aircraft_list = aircraft_list

        self.clock = pygame.time.Clock()

        # Professional radar palette
        self.bg_color = (8, 12, 14)
        self.radar_green = (0, 255, 140)
        self.taxi_color = (70, 90, 90)
        self.runway_color = (140, 140, 140)
        self.tag_bg = (15, 25, 28)

        self.font = pygame.font.SysFont("consolas", 14)
        self.tag_font = pygame.font.SysFont("consolas", 13)
        self.airport_font = pygame.font.SysFont("consolas", 18, bold=True)

        self.radar_center = (550, 350)
        self.radar_radius = 320

        self.bus = bus
        self.comms_log = []
        self.max_log_lines = 25

        bus.register_listener(self.log_message)

    # ---------------------------------------------------------
    def draw_background(self):
        self.screen.fill(self.bg_color)

    def log_message(self, message):

        # Convert structured message into readable string
        if message.type == "CLEARANCE_TAXI":
            text = f"{message.sender} → {message.receiver}: Taxi via {message.content['route']}"
        elif message.type == "CLEARANCE_TAKEOFF":
            text = f"{message.sender} → {message.receiver}: Cleared for takeoff RWY {message.content['runway']}"
        else:
            text = f"{message.sender} → {message.receiver}: {message.type}"

        self.comms_log.append(text)

        if len(self.comms_log) > 200:
            self.comms_log.pop(0)

    def draw_comms_panel(self):

        panel_x = 800
        panel_width = 500

        # Background
        pygame.draw.rect(self.screen,
                        (10, 18, 22),
                        (panel_x, 0, panel_width, self.height))

        pygame.draw.line(self.screen,
                        (0, 80, 60),
                        (panel_x, 0),
                        (panel_x, self.height), 2)

        # Title
        title = self.airport_font.render("ATC COMMUNICATIONS", True, self.radar_green)
        self.screen.blit(title, (panel_x + 15, 20))

        # Messages
        y_offset = 70
        recent = self.comms_log[-self.max_log_lines:]

        for line in recent:
            text = self.tag_font.render(line, True, (200, 200, 200))
            self.screen.blit(text, (panel_x + 15, y_offset))
            y_offset += 20

    # ---------------------------------------------------------
    def draw_radar_grid(self):

        cx, cy = self.radar_center

        for r in range(80, self.radar_radius, 80):
            pygame.draw.circle(self.screen, (0, 60, 40), (cx, cy), r, 1)

        pygame.draw.line(self.screen, (0, 70, 50),
                         (cx - self.radar_radius, cy),
                         (cx + self.radar_radius, cy), 1)

        pygame.draw.line(self.screen, (0, 70, 50),
                         (cx, cy - self.radar_radius),
                         (cx, cy + self.radar_radius), 1)

        angle = pygame.time.get_ticks() * 0.05
        sweep_x = cx + self.radar_radius * math.cos(math.radians(angle))
        sweep_y = cy + self.radar_radius * math.sin(math.radians(angle))

        pygame.draw.line(self.screen, (0, 200, 120),
                         (cx, cy), (sweep_x, sweep_y), 1)

    # ---------------------------------------------------------
    def draw_edges(self):

        for edge in self.world.edges:

            start = (edge.start_node.x, edge.start_node.y)
            end = (edge.end_node.x, edge.end_node.y)

            if edge.category == "runway":
                pygame.draw.line(self.screen, self.runway_color, start, end, 12)

                segments = 20
                for i in range(segments):
                    if i % 2 == 0:
                        sx = start[0] + (end[0] - start[0]) * i / segments
                        sy = start[1] + (end[1] - start[1]) * i / segments
                        ex = start[0] + (end[0] - start[0]) * (i + 1) / segments
                        ey = start[1] + (end[1] - start[1]) * (i + 1) / segments
                        pygame.draw.line(self.screen, (220, 220, 220),
                                         (sx, sy), (ex, ey), 2)

            else:
                color = self.taxi_color
                if edge.occupied_by:
                    color = (255, 60, 60)

                pygame.draw.line(self.screen, color, start, end, 2)

    # ---------------------------------------------------------
    def draw_airport_labels(self):

        for edge in self.world.edges:

            start = edge.start_node
            end = edge.end_node

            mid_x = (start.x + end.x) / 2
            mid_y = (start.y + end.y) / 2

            dx = end.x - start.x
            dy = end.y - start.y
            angle = math.degrees(math.atan2(dy, dx))

            # RUNWAY LABEL
            if edge.category == "runway":
                label = "RWY 09/27"
                text = self.airport_font.render(label, True, (255, 255, 255))
                rotated = pygame.transform.rotate(text, -angle)
                rect = rotated.get_rect(center=(mid_x, mid_y))
                self.screen.blit(rotated, rect)

            # TAXIWAY ECHO LABEL
            if edge.category == "taxiway":
                label = "E"
                text = self.airport_font.render(label, True, (255, 255, 0))
                rotated = pygame.transform.rotate(text, -angle)
                rect = rotated.get_rect(center=(mid_x, mid_y))
                self.screen.blit(rotated, rect)

        # TERMINAL LABEL
        terminal_text = self.airport_font.render("TERMINAL 1", True, (255, 255, 255))
        self.screen.blit(terminal_text, (70, 220))

    # ---------------------------------------------------------
    def draw_nodes(self):
        for node in self.world.nodes.values():
            pygame.draw.circle(self.screen,
                               (0, 120, 80),
                               (node.x, node.y), 3)

    # ---------------------------------------------------------
    def draw_aircraft(self):

        for aircraft in self.aircraft_list:

            x = aircraft.x
            y = aircraft.y

            # Determine heading angle
            if aircraft.current_edge:
                start = aircraft.current_edge.start_node
                end = aircraft.current_edge.end_node
                angle = math.atan2(end.y - start.y, end.x - start.x)

            elif aircraft.current_state == "AIRBORNE":
                angle = -math.pi / 2  # pointing upward (temporary)

            else:
                angle = 0

            pygame.draw.circle(self.screen,
                               (0, 100, 70),
                               (int(x), int(y)),
                               20, 1)

            size = 8
            points = [
                (x + size * math.cos(angle),
                 y + size * math.sin(angle)),
                (x + size * math.cos(angle + 2.5),
                 y + size * math.sin(angle + 2.5)),
                (x + size * math.cos(angle - 2.5),
                 y + size * math.sin(angle - 2.5)),
            ]

            pygame.draw.polygon(self.screen,
                                self.radar_green,
                                points)

            self.draw_data_tag(aircraft, x, y)

    # ---------------------------------------------------------
    def draw_data_tag(self, aircraft, x, y):

        tag_x = x + 25
        tag_y = y - 25

        pygame.draw.rect(self.screen,
                         self.tag_bg,
                         (tag_x, tag_y, 140, 85), 0)

        pygame.draw.rect(self.screen,
                         (0, 120, 80),
                         (tag_x, tag_y, 140, 85), 1)

        gs_knots = aircraft.speed * 1.94384
        vs_fpm = aircraft.vertical_speed * 196.85
        alt_ft = aircraft.altitude * 3.28084

        lines = [
            aircraft.callsign,
            aircraft.current_state,
            f"GS {int(gs_knots)} kt",
            f"VS {int(vs_fpm)} fpm",
            f"ALT {int(alt_ft)} ft"
        ]

        offset = 5
        for line in lines:
            text = self.tag_font.render(line,
                                        True,
                                        self.radar_green)
            self.screen.blit(text,
                             (tag_x + 6, tag_y + offset))
            offset += 18

    # ---------------------------------------------------------
    def draw_status_bar(self):

        pygame.draw.rect(self.screen,
                         (12, 20, 24),
                         (0, 660, self.width, 40))

        text = self.font.render(
            f"Aircraft: {len(self.aircraft_list)} | "
            f"Simulation Time: {pygame.time.get_ticks() // 1000}s",
            True,
            self.radar_green
        )

        self.screen.blit(text, (20, 670))

    # ---------------------------------------------------------
    def update(self):

        self.draw_background()
        self.draw_radar_grid()
        self.draw_edges()
        self.draw_airport_labels()  
        self.draw_nodes()
        self.draw_aircraft()
        self.draw_status_bar()
        self.draw_comms_panel() 
        pygame.display.flip()
        self.clock.tick(60)