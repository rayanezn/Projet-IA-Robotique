from robot import *

nb_robots = 0
debug = True

class Robot_player(Robot):
    team_name = "Avoider"
    robot_id = -1
    iteration = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        
        # --- PRE-PROCESSING (Fourni) ---
        sensor_to_wall = []
        sensor_to_robot = []
        for i in range (0,8):
            if sensor_view[i] == 1: # Mur
                sensor_to_wall.append( sensors[i] )
                sensor_to_robot.append(1.0)
            elif sensor_view[i] == 2: # Robot
                sensor_to_wall.append( 1.0 )
                sensor_to_robot.append( sensors[i] )
            else: # Vide
                sensor_to_wall.append(1.0)
                sensor_to_robot.append(1.0)

        # --- BRAITENBERG AVOIDER ---


        # --- TRANSLATION : éviter murs + robots ---
        translation = 1 - (sum(sensor_to_wall) + sum(sensor_to_robot))

        # --- ROTATION : différence gauche / droite ---
        left_sensors  = sensor_to_wall[0:4] + sensor_to_robot[0:4]
        right_sensors = sensor_to_wall[4:8] + sensor_to_robot[4:8]

        rotation = (sum(right_sensors) - sum(left_sensors))

        self.iteration += 1        
        return translation, rotation, False