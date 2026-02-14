from robot import *

nb_robots = 0
debug = True

class Robot_player(Robot):

    team_name = "BotHater"
    robot_id = -1
    iteration = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        
        # --- PRE-PROCESSING ---
        # On prépare une liste de capteurs qui ne "voit" que les robots
        sensor_to_robot = []
        
        for i in range (0,8):
            if sensor_view[i] == 2: # C'est un ROBOT
                # On garde la vraie distance (plus c'est petit, plus ça fait peur)
                sensor_to_robot.append( sensors[i] )
                
            else: # C'est un MUR (1) ou du VIDE (0)
                # On ignore totalement les murs en mettant la distance au max (1.0)
                sensor_to_robot.append( 1.0 )

        # --- LOGIQUE BRAITENBERG (Hate Bot) ---
        
        # 1. Translation : 
        # On avance vite si pas de ROBOT devant.
        # On utilise les capteurs avant (Front-Left, Front, Front-Right)
        translation = sensor_to_robot[sensor_front_left] + sensor_to_robot[sensor_front] + sensor_to_robot[sensor_front_right]

        # 2. Rotation : Évitement (Fuite)c
        # On utilise UNIQUEMENT la liste sensor_to_robot
        
        
        dist_left = sensor_to_robot[sensor_front_left] + sensor_to_robot[sensor_left] + sensor_to_robot[sensor_rear_left]
        
        # Moyenne des capteurs Droite
        dist_right = sensor_to_robot[sensor_front_right] + sensor_to_robot[sensor_right] + sensor_to_robot[sensor_rear_right]
        
        # Formule d'ÉVITEMENT : (Gauche - Droite)
        # Si un robot est à gauche (dist_left petit), le résultat est négatif -> Tourne à Droite (fuite)
        rotation = dist_left - dist_right

        self.iteration += 1        
        return translation, rotation, False