from robot import *

nb_robots = 0
debug = True

class Robot_player(Robot):
    team_name = "BotLover"
    robot_id = -1
    iteration = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        
        # --- PRE-PROCESSING ---
        # On trie pour ne garder que les ROBOTS
        sensor_to_wall = []
        sensor_to_robot = []
        
        for i in range (0,8):
            if sensor_view[i] == 1: # C'est un MUR
                sensor_to_wall.append( sensors[i] )
                # IMPORTANT : On dit 1.0 (loin) dans sensor_to_robot car on veut IGNORER le mur
                sensor_to_robot.append(1.0) 
                
            elif sensor_view[i] == 2: # C'est un ROBOT
                sensor_to_wall.append( 1.0 )
                # On garde la vraie distance pour le robot
                sensor_to_robot.append( sensors[i] ) 
                
            else: # C'est VIDE
                sensor_to_wall.append(1.0)
                sensor_to_robot.append(1.0)

        # --- BRAITENBERG LOVE BOT ---

        # 1. Translation : Vitesse
        # tant qu'on voit un robot devant, on avance.
        translation = 1.0

        # 2. Rotation : Attraction vers les robots
        # On utilise UNIQUEMENT la liste sensor_to_robot
        
       
        dist_left = sensor_to_robot[sensor_front_left] + sensor_to_robot[sensor_left] + sensor_to_robot[sensor_rear_left]
        
       
        dist_right = sensor_to_robot[sensor_front_right] + sensor_to_robot[sensor_right] + sensor_to_robot[sensor_rear_right]
        
        # Formule d'ATTRACTION : (Droite - Gauche)
        # Si un robot est à gauche (dist_left est petit, ex: 0.2)
        # 1.0 - 0.2 = +0.8 -> Rotation POSITIVE -> Tourne à GAUCHE (vers le robot)
        rotation = dist_right - dist_left 

        self.iteration += 1        
        return translation, rotation, False