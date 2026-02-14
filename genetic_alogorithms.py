from robot import *
import math
import random

nb_robots = 0
debug = False

class Robot_player(Robot):

    team_name = "Genetic_Robust"
    robot_id = -1

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a", evaluations=500, it_per_evaluation=400, replay_iterations=1000):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

        # Paramètres de simulation
        self.max_evals = evaluations
        self.it_per_evaluation = it_per_evaluation
        self.replay_iterations = replay_iterations

        # Gestion des 3 orientations (Nouvelle logique)
        self.sub_trial = 0
        self.orientations = [0, 120, 240] # Les 3 angles de départ
        
        # Etat interne
        self.replay_mode = False
        self.eval_id = 0
        self.iter_in_eval = 0     # Compteur global pour l'évaluation
        self.iter_in_subtrial = 0 # Compteur local pour l'orientation actuelle
        self.iter_in_replay = 0

        # Score
        self.score_eval = 0.0     # Score cumulé sur les 3 essais

        # Algo genetique (1+1)
        self.parentParam = self.random_param()
        self.parentScore = float("-inf")
        
        # On commence par tester un enfant (mutation du parent aléatoire)
        self.param = self.mutate_one(self.parentParam)

        # Meilleur global
        self.bestScore = float("-inf")
        self.bestParam = self.param[:]
        self.bestEval = -1

        print("# eval_id, score_candidat, best_so_far")

        # CSV
        # CSV - Fichier unique fixe
        self.csv_name = "results_genetic.csv" 
        
        # Mode "w" : Écrase le fichier précédent à chaque démarrage du programme
        # Mode "a" : Ajoute à la suite (mais attention, l'en-tête sera réécrit)
        self.csv = open(self.csv_name, "w", encoding="utf-8")
        self.csv.write("eval,score,best,p0,p1,p2,p3,p4,p5,p6,p7\n")
        self.csv.flush()

    def reset(self):
        super().reset()
        # C'est ici qu'on change l'orientation pour le sous-essai
        # On force l'angle du robot
        self.theta = self.orientations[self.sub_trial]
        
        # Reset des compteurs locaux si besoin (mais géré dans step)
        pass

    def random_param(self):
        return [random.randint(-1, 1) for _ in range(8)]

    def mutate_one(self, p):
        q = p[:]
        idx = random.randrange(len(q))
        old = q[idx]
        choices = [-1, 0, 1]
        choices.remove(old)
        q[idx] = random.choice(choices)
        return q

    def control(self, sensors):
        # Calcul des commandes moteur
        t = math.tanh(self.param[0] + self.param[1]*sensors[sensor_front_left] + self.param[2]*sensors[sensor_front] + self.param[3]*sensors[sensor_front_right])
        r = math.tanh(self.param[4] + self.param[5]*sensors[sensor_front_left] + self.param[6]*sensors[sensor_front] + self.param[7]*sensors[sensor_front_right])
        return t, r

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        
        # --- MODE REPLAY (Une fois la recherche finie) ---
        if self.replay_mode:
            translation, rotation = self.control(sensors)
            self.iter_in_replay += 1
            if self.iter_in_replay >= self.replay_iterations:
                self.iter_in_replay = 0
                return 0, 0, True # Reset infini pour la démo
            return translation, rotation, False

        # --- MODE GENETIQUE (Evaluation) ---
        
        # 1. Calcul des commandes
        translation, rotation = self.control(sensors)

        # 2. Accumulation du score (Méthode manuelle robuste)
        # On évite le score nul au démarrage (iter > 0)
        if self.iter_in_subtrial > 0:
            self.score_eval += translation * (1.0 - abs(rotation))

        # 3. Gestion du temps et des sous-essais
        limit_per_orientation = self.it_per_evaluation // 3
        
        # On incrémente les compteurs
        self.iter_in_subtrial += 1
        self.iter_in_eval += 1

        # Vérification de la fin d'un sous-essai (orientation)
        if self.iter_in_subtrial >= limit_per_orientation:
            
            # CAS A : Il reste des orientations à tester (0 ou 1)
            if self.sub_trial < 2:
                self.sub_trial += 1         # On passe à l'angle suivant
                self.iter_in_subtrial = 0   # On reset le compteur local
                return 0, 0, True           # RESET POSITION (Appelle self.reset())
            
            # CAS B : Fin du 3ème essai (Evaluation complète terminée)
            else:
                childScore = self.score_eval
                
                # --- LOGIQUE DE SELECTION (1+1) ---
                
                # Si l'enfant est meilleur (ou si premier essai), il devient le nouveau parent
                if self.parentScore == float("-inf") or childScore > self.parentScore:
                    self.parentParam = self.param[:]
                    self.parentScore = childScore
                else:
                    # Sinon, on garde l'ancien parent (on annule la mutation)
                    # Note : self.param sera écrasé par la mutation du parent juste après
                    pass

                # Mise à jour du RECORD GLOBAL
                if self.parentScore > self.bestScore:
                    self.bestScore = self.parentScore
                    self.bestParam = self.parentParam[:]
                    self.bestEval = self.eval_id
                    print(f"[NEW BEST] Eval {self.eval_id}: Score={self.bestScore:.2f} Params={self.bestParam}")

                # Affichage console (CSV format)
                print(f"{self.eval_id}, {childScore:.2f}, {self.bestScore:.2f}")

                # Ecriture fichier CSV
                p = self.param # On sauvegarde les params qui viennent d'être testés
                self.csv.write(f"{self.eval_id},{childScore},{self.bestScore},"
                               f"{p[0]},{p[1]},{p[2]},{p[3]},{p[4]},{p[5]},{p[6]},{p[7]}\n")
                self.csv.flush()

                # --- PREPARATION GENERATION SUIVANTE ---
                self.eval_id += 1
                
                # Vérifier si c'est la fin de l'expérience
                if self.eval_id >= self.max_evals:
                    self.csv.write(f"best score = {self.bestScore}, best param = {self.bestParam}\n")
                    self.csv.close()
                    self.replay_mode = True
                    self.param = self.bestParam[:] # On charge le champion
                    
                    print("\n=== GENETIC FINISHED ===")
                    print(f"Best Score: {self.bestScore}")
                    print(f"Best Params: {self.bestParam}")
                    
                    # Reset propre pour le replay
                    self.sub_trial = 0 
                    self.iter_in_eval = 0
                    return 0, 0, True

                # Mutation : On repart TOUJOURS du parent (le meilleur actuel)
                self.param = self.mutate_one(self.parentParam)

                # Reset complet pour le nouvel individu
                self.sub_trial = 0          # Retour à l'orientation 0
                self.iter_in_subtrial = 0
                self.iter_in_eval = 0
                self.score_eval = 0.0       # Reset du score cumulé
                
                return 0, 0, True # Reset position pour le nouveau candidat

        return translation, rotation, False