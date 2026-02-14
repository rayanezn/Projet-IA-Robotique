from robot import *
import math
import random

nb_robots = 0

class Robot_player(Robot):

    team_name = "Optimizer"
    robot_id = -1
    iteration = 0

    # Paramètres de recherche
    param = []
    best_param = []
    best_score = -1.0
    best_tuple = (0, [], 0) # (score, paramètres, numéro_essai)

    it_per_evaluation = 400
    trial = 0
    max_trials = 500  # On fixe le nombre de comportements à évaluer

    x_0 = 0
    y_0 = 0
    theta_0 = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a", evaluations=0, it_per_evaluation=0):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        self.x_0 = x_0
        self.y_0 = y_0
        self.theta_0 = theta_0
        
        # Initialisation du premier cerveau
        self.param = [random.randint(-1, 1) for i in range(8)]
        
        # On utilise les variables passées en argument si elles existent
        if evaluations > 0: self.max_trials = evaluations
        if it_per_evaluation > 0: self.it_per_evaluation = it_per_evaluation
        
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        
        if self.iteration % self.it_per_evaluation == 0 :  #toutes les 400 itérations
            if  self.iteration > 0 :
            
                current_score = self.log_sum_of_translation * (1 - abs(self.log_sum_of_rotation))
                
            
                if current_score > self.best_score:
                    self.best_score = current_score
                    self.best_param = self.param[:] 
                    self.best_tuple = (self.best_score, self.best_param, self.trial)
                    print(f">>> NOUVEAU MEILLEUR : Score={self.best_score:.2f} (Essai {self.trial})")

                # 3. on passe a la strat suivante 
                self.trial += 1
                if self.trial < self.max_trials:
                    # On continue la recherche : nouveau jeu d param aléatoire
                    self.param = [random.randint(-1, 1) for i in range(8)]
                    print(f"Essai {self.trial}/{self.max_trials} en cours...")
                    self.iteration += 1 
                    return 0, 0, True # Reset position
                else:
                    # Fin des 500 essais : on garde le meilleur pour toujours
                    print(f"RECHERCHE TERMINEE. Meilleur score final : {self.best_score:.2f}")
                    print(f"Best param : {self.best_param}")
                    print(f"son trial : {self.best_tuple[2]}")
                    self.param = self.best_param
                    return 0, 0, False # On ne reset plus, on laisse rouler le champion

        # --- CONTROLEUR (RESEAU DE NEURONES) ---
        # Calcul des commandes basé sur les paramètres actuels (self.param)
        translation = math.tanh(self.param[0] + self.param[1] * sensors[sensor_front_left] + 
                                self.param[2] * sensors[sensor_front] + self.param[3] * sensors[sensor_front_right])
        
        rotation = math.tanh(self.param[4] + self.param[5] * sensors[sensor_front_left] + 
                             self.param[6] * sensors[sensor_front] + self.param[7] * sensors[sensor_front_right])

        self.iteration += 1
        return translation, rotation, False
