from robot import *

nb_robots = 0
debug = True

class Robot_player(Robot):
    team_name = "WallHater"
    robot_id = -1
    iteration = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        
        # --- PRE-PROCESSING ---
        sensor_to_wall = []
        sensor_to_robot = []
        for i in range (0,8):
            if sensor_view[i] == 1:
                sensor_to_wall.append( sensors[i] )
                sensor_to_robot.append(1.0)
            elif sensor_view[i] == 2:
                sensor_to_wall.append( 1.0 ) # Robot = Invisible (vide)
                sensor_to_robot.append( sensors[i] )
            else:
                sensor_to_wall.append(1.0)
                sensor_to_robot.append(1.0)

        # --- BRAITENBERG HATE WALL ---

        translation = (sum(sensor_to_wall))

        # --- ROTATION : différence gauche / droite ---
        left_sensors  = sensor_to_wall[0:4] 
        right_sensors = sensor_to_wall[4:8] 
        
        # Formule Standard (Gauche - Droite) sur les murs uniquement
        rotation =  (sum(left_sensors) - sum(right_sensors))

        self.iteration += 1        
        return translation, rotation, False