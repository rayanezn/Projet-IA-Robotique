# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant/e : Juba   YAHIAOUI 21312266
#  Prénom Nom No_étudiant/e : Rayane ZANE   21305648
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)



from robot import *
import random
import math

nb_robots = 0

class Robot_player(Robot):

    team_name = "CarlsenMagnus"  # vous pouvez modifier le nom de votre équipe
    robot_id = -1
    memory = 0  # on va l'utiliser comme compteur / mode

    LATERAL_SENSORS = [sensor_front_left, sensor_left, sensor_front_right, sensor_right]
    NON_LATERAL_SENSORS = [sensor_front, sensor_rear_left, sensor_rear, sensor_rear_right]

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

        # paramètres "génétiques"
        self.param = [1, 1, 1, 1, 1, -1, -1, 1]

    def reset(self):
        super().reset()
        self.memory = 0  # on réinitialise le mode

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        # --- 0) Gestion de la mémoire : alterner les modes tous les 50 pas ---
        # memory = compteur, et on déduit le mode à partir de lui
        self.memory += 1
        if self.memory > 1000:
            self.memory = 0
        mode_agressif = 1 if (self.memory // 50) % 2 == 1 else 0

        # --- 1) robot détecté : comportement dépendant du mode ---
        if sensor_view is not None and any(view == 2 for view in sensor_view):
            # on récupère les directions où il y a un robot
            enemy_dirs = [i for i, v in enumerate(sensor_view) if v == 2]
            dir_idx = random.choice(enemy_dirs)

            # dir_idx: 0=front, 1=front-left, 2=left, 3=rear-left, 4=rear,
            #          5=rear-right, 6=right, 7=front-right (selon la convention du projet)
            angle = dir_idx * 45
            if angle > 180:
                angle -= 360
            rotation = angle / 180.0

            if mode_agressif:
                # mode agressif : on va vers l’robot
                translation = 1.0
                return translation, rotation, False
            else:
                # mode prudent : on fuit (on inverse la rotation)
                translation = 1.0
                return translation, -rotation, False

        # --- 2) Mur latéral : suivi de mur amélioré ---
        if sensor_view is not None and any(sensor_view[i] == 1 for i in self.LATERAL_SENSORS):
            if random.random() < 0.9:
                # suivre le mur
                thr = sensors[sensor_front]
                translation = 0.5 + 0.5 * (1.0 - thr)  # avance un peu plus si c’est dégagé
                rot_left = sensors[sensor_left] + sensors[sensor_front_left]
                rot_right = sensors[sensor_right] + sensors[sensor_front_right]
                rotation = (rot_left - rot_right) * 0.5
                rotation = max(min(rotation, 1.0), -1.0)
                return translation, rotation, False
            else:
                # petite probabilité d’évitement aléatoire
                free_dirs = [i for i in range(8) if sensor_view[i] != 1]
                if not free_dirs:
                    return 0.5, random.uniform(-1.0, 1.0), False
                dir_idx = random.choice(free_dirs)
                angle = dir_idx * 45
                if angle > 180:
                    angle -= 360
                rotation = angle / 180.0
                return 0.8, rotation, False

        # --- 3) Mur non-latéral : évitement classique ---
        if sensor_view is not None and any(sensor_view[i] == 1 for i in self.NON_LATERAL_SENSORS):
            free_dirs = [i for i in range(8) if sensor_view[i] != 1]
            if not free_dirs:
                return 0.5, random.uniform(-1.0, 1.0), False
            dir_idx = random.choice(free_dirs)
            angle = dir_idx * 45
            if angle > 180:
                angle -= 360
            rotation = angle / 180.0
            return 0.8, rotation, False

        # --- 4) Comportement "génétique" par défaut ---
        t = math.tanh(
            self.param[0]
            + self.param[1] * sensors[sensor_front_left]
            + self.param[2] * sensors[sensor_front]
            + self.param[3] * sensors[sensor_front_right]
        )
        r = math.tanh(
            self.param[4]
            + self.param[5] * sensors[sensor_front_left]
            + self.param[6] * sensors[sensor_front]
            + self.param[7] * sensors[sensor_front_right]
        )

        # on peut booster un peu la translation en mode agressif
        if mode_agressif:
            t = max(min(t + 0.3, 1.0), -1.0)

        return t, r, False
