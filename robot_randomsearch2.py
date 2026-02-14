from robot import *
import math
import random

nb_robots = 0

class Robot_player(Robot):

    team_name = "Optimizer_Robust"
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
        self.sub_trial = 0 # Sous-essai : 0, 1, 2 pour les 3 orientations imposées
        self.orientations = [0, 120, 240] # Orientations imposées pour les sous-essais
        self.cumulative_score = 0.0 # <--- LIGNE AJOUTÉE : Accumulateur pour l'Exo 2
        # Ouvre un fichier pour écrire les résultats (mode 'w' = write)
        self.log_file = open("resultats_random.csv", "w")
        
        # Initialisation du premier cerveau
        self.param = [random.randint(-1, 1) for i in range(8)]
        
        # On utilise les variables passées en argument si elles existent
        if evaluations > 0: self.max_trials = evaluations
        if it_per_evaluation > 0: self.it_per_evaluation = it_per_evaluation
        
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):


        if self.iteration % (self.it_per_evaluation // 3)== 0 : 
            if  self.iteration > 0 :
                current_score = self.log_sum_of_translation * (1 - abs(self.log_sum_of_rotation))
                
    
                self.cumulative_score += current_score # On ajoute le score du passage actuel
                
                if self.sub_trial < 2: # S'il reste des orientations à tester (0 et 1)
                    self.sub_trial += 1
                    self.iteration += 1 
                    return 0, 0, True # On reset SANS changer les paramètres (param)
                
                # Si on arrive ici, c'est que sub_trial == 2 (3ème essai fini)
                # On remplace current_score par la somme totale pour la comparaison
                current_score = self.cumulative_score 
                self.sub_trial = 0 # Reset pour le prochain set de paramètres
                self.cumulative_score = 0 # Reset pour le prochain set de paramètres
                

                # 2. Comparaison et sauvegarde du meilleur
                if current_score > self.best_score:
                    self.best_score = current_score
                    self.best_param = self.param[:] # Copie de la liste
                    self.best_tuple = (self.best_score, self.best_param, self.trial)
                    print(f">>> NOUVEAU MEILLEUR ROBUSTE : Score={self.best_score:.2f} (Essai {self.trial})")

                #EXO4 :  On écrit : numéro_essai, score_actuel, meilleur_score_global
                self.log_file.write(f"{self.trial},{current_score},{self.best_score}\n")
                self.log_file.flush() # Force l'écriture sur le disque immédiatement

                # 3. Choix de la suite
                self.trial += 1
                if self.trial < self.max_trials:
                    self.param = [random.randint(-1, 1) for i in range(8)]
                    print(f"Essai {self.trial}/{self.max_trials} en cours...")
                    self.iteration += 1 
                    return 0, 0, True # Reset position
                else:
                    print(f"RECHERCHE TERMINEE. Meilleur score final : {self.best_score:.2f}")
                    print(f"Best param : {self.best_param}")
                    self.param = self.best_param
                    return 0, 0, False 
                
        translation = math.tanh(self.param[0] + self.param[1] * sensors[sensor_front_left] + 
                                self.param[2] * sensors[sensor_front] + self.param[3] * sensors[sensor_front_right])
        
        rotation = math.tanh(self.param[4] + self.param[5] * sensors[sensor_front_left] + 
                             self.param[6] * sensors[sensor_front] + self.param[7] * sensors[sensor_front_right])

        self.iteration += 1
        return translation, rotation, False
    
    def reset(self):
        super().reset() 
        self.theta = self.orientations[self.sub_trial]