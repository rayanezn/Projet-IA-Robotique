# 🤖 Projet Robotique – Comportements Réactifs et Paint Wars

## Description
Ce projet regroupe les TPs et un projet final de robotique, centrés sur le comportement autonome de robots dans une arène.  
Les objectifs principaux sont :

- Programmer des comportements simples et réactifs de type Braitenberg.
- Implémenter une architecture de subsomption pour combiner plusieurs comportements.
- Optimiser les comportements via recherche aléatoire et algorithmes génétiques.
- Créer un projet final compétitif "Paint Wars" où deux équipes de robots s'affrontent pour contrôler des zones de l’arène.

---

## Contenu du projet

### TP 1 – Comportements réactifs
- Exercice 1 : Comportements de Braitenberg
  - Éviter les obstacles, aller vers les murs ou les robots selon le comportement choisi.
  - Fichiers créés :  
    `robot_braitenberg_avoider.py`, `robot_braitenberg_loveWall.py`, `robot_braitenberg_hateWall.py`, `robot_braitenberg_loveBot.py`, `robot_braitenberg_hateBot.py`
- Exercice 2 : Architecture de subsomption
  - Combinaison de comportements pour poursuivre les robots tout en évitant les obstacles.  
  - Fichier : `robot_subsomption.py`

### TP 2 – Optimisation de comportements
- Recherche aléatoire pour améliorer la translation et minimiser la rotation.  
  Fichier : `robot_randomsearch.py`
- Évaluation avec différentes conditions initiales.  
  Fichier : `randomsearch2.py`
- Algorithme génétique pour optimiser les paramètres du robot.  
  Fichier : `genetic_algorithms.py`
- Comparaison des résultats et visualisation via graphes.

### Projet final – Paint Wars
- Deux équipes de 4 robots s’affrontent pour contrôler une arène découpée en cases.
- Comportements utilisés :
  - Architecture de subsomption ou arbre de décision
  - Comportements Braitenberg optimisés
- Fichiers principaux :
  - `robot_challenger.py` – nos robots (en binome)
  - `robot_challenger.py` - robots du prof
  - `config_Paintwars.py` – configuration de l’arène
  - `tetracomposibot.py` – programme principal
  - `go_tournament` – script pour lancer les matchs
  - `go_tournament_eval` – script pour lancer les matchs avec plus d'arènes

---

## Exécution
Lancer le projet avec la configuration n (de 0 à 4) :  

```bash
python tetracomposibot.py config_Paintwars n
```

Lancer le tournoi :

```bash
sh go_tournament_eval
```

## Auteurs

- Rayane ZANE
- Juba Yahiaoui

Sorbonne Université – LU3IN025 : IA et Jeux

