from robot import *

nb_robots = 0
debug = True

class Robot_player(Robot):
    team_name = "WallLover"
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
                sensor_to_wall.append( 1.0 ) # On ignore le robot (distance max)
                sensor_to_robot.append( sensors[i] )
            else:
                sensor_to_wall.append(1.0)
                sensor_to_robot.append(1.0)

        # --- BRAITENBERG LOVE WALL ---

        # 1. Translation: Vitesse constante (ou ralentir si mur très proche pour "embrasser" le mur sans rebondir trop fort)
        translation = 0.8 

        # 2. Rotation: Attraction
        # On utilise UNIQUEMENT sensor_to_wall
        wall_left = sensor_to_wall[sensor_front_left] + sensor_to_wall[sensor_left] + sensor_to_wall[sensor_rear_left]
        wall_right = sensor_to_wall[sensor_front_right] + sensor_to_wall[sensor_right] + sensor_to_wall[sensor_rear_right]
        
        # Formule inversée (Droite - Gauche) :
        # Si mur à gauche (valeur faible), le résultat est positif -> Tourne à Gauche (vers le mur)
        rotation = wall_right - wall_left

        self.iteration += 1        
        return translation, rotation, False