from robot import *

nb_robots = 0
debug = True

class Robot_player(Robot):

    team_name = "SubsumptionBot"
    robot_id = -1
    iteration = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    # --- COMPORTEMENT 1 : CRUISE (Aller tout droit) ---
    def behavior_exploration(self):
        # Avance à vitesse moyenne, pas de rotation
        return 1, 0.0

    # --- COMPORTEMENT 2 : HATE WALL (Évitement de mur type Braitenberg) ---
    def behavior_avoid_wall(self, sensor_to_wall):
        # Vitesse : Ralentit si mur devant
        translation = (sum(sensor_to_wall))

        # --- ROTATION : différence gauche / droite ---
        left_sensors  = sensor_to_wall[0:4] 
        right_sensors = sensor_to_wall[4:8] 
        
        # Formule Standard (Gauche - Droite) sur les murs uniquement
        rotation =  (sum(left_sensors) - sum(right_sensors))
        
        return translation, rotation

    # --- COMPORTEMENT 3 : LOVE BOT (Attraction robot type Braitenberg) ---
    def behavior_chase_robot(self, sensor_to_robot):
        # Vitesse : Fonce
        translation = 1.0

        # 2. Rotation : Attraction vers les robots
        # On utilise UNIQUEMENT la liste sensor_to_robot
        
       
        dist_left = sensor_to_robot[sensor_front_left] + sensor_to_robot[sensor_left] + sensor_to_robot[sensor_rear_left]
        
       
        dist_right = sensor_to_robot[sensor_front_right] + sensor_to_robot[sensor_right] + sensor_to_robot[sensor_rear_right]
        
        # Formule d'ATTRACTION : (Droite - Gauche)
        # Si un robot est à gauche (dist_left est petit, ex: 0.2)
        # 1.0 - 0.2 = +0.8 -> Rotation POSITIVE -> Tourne à GAUCHE (vers le robot)
        rotation = dist_right - dist_left 
        
        return translation, rotation


    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        
        # 1. Pre-processing des senseurs
        sensor_to_wall = []
        sensor_to_robot = []
        
        # Variables pour détecter si les conditions d'activation sont remplies
        min_dist_wall = 1.0
        robot_detected = False

        for i in range(8):
            if sensor_view[i] == 1: # Mur
                sensor_to_wall.append(sensors[i])
                sensor_to_robot.append(1.0)
                if sensors[i] < min_dist_wall: min_dist_wall = sensors[i]
            
            elif sensor_view[i] == 2: # Robot
                sensor_to_wall.append(1.0)
                sensor_to_robot.append(sensors[i])
                robot_detected = True # On a vu un robot !
            
            else: # Vide
                sensor_to_wall.append(1.0)
                sensor_to_robot.append(1.0)

        # 2. ARCHITECTURE DE SUBSOMPTION
        # On teste les conditions du plus prioritaire au moins prioritaire
        
        # -- NIVEAU 1 : SURVIE (Evitement de mur) --
        # Seuil d'activation : Si un mur est à moins de 30% de la portée max
        if min_dist_wall < 0.3:
            translation, rotation = self.behavior_avoid_wall(sensor_to_wall)
            if debug and self.robot_id == 0 and self.iteration % 50 == 0:
                print("Robot 0 State: AVOIDING WALL")
        
        # -- NIVEAU 2 : CHASSE (Suivi de robot) --
        # Condition : Si on n'est pas en danger (mur) ET qu'on voit un robot
        elif robot_detected:
            translation, rotation = self.behavior_chase_robot(sensor_to_robot)
            if debug and self.robot_id == 0 and self.iteration % 50 == 0:
                print("Robot 0 State: CHASING ROBOT")

        # -- NIVEAU 3 : Exploration --
        # Défaut : Si rien d'autre ne s'active
        else:
            translation, rotation = self.behavior_exploration()
            if debug and self.robot_id == 0 and self.iteration % 50 == 0:
                print("Robot 0 State: Exploration")

        self.iteration += 1
        return translation, rotation, False