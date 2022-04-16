# Rapport technique Smardlino

En évaluant le projet, il a été décidé de commencer par apprendre comment fonctionne arduino.

## 1. Arduino - Prise en mains

Le premier but est de savoir comment faire fonctionner arduino.

Une led RGB est installée et le but est de l'allumer.

Puis, un joystick est installé et le but est de lire les valeurs du joystick par un Serial.print.

### Problème

Quelles sont les valeurs renvoyées par le joystick?

### Solution

Un simple Serial.print et tester.

## 2. Arduino - Plus profond

Une fois la prise en d'arduino effectuée, il est décider d'approfondir la manipulation arduino.

Avec un joystick et une led connectée, il est possible de changer la couleur de la led.

### Problème

Comment changer la couleur de la led depuis un joystick?

### Solution

Le joystick est vu comme un cercle:

- prendre l'angle comme valeur hue.
- prendre la "distance du joystick par rapprot à son centre" comme valeur saturation.

Puis convertir la valeur HSV en RGB.

#### Problème rencontré

La convertion HSV => RGB ne fonctionne pas.

#### Solution

Beaucoup de Serial.print, pour au final faire un script pyhton exécutant la même chose sur un GUI desktop.

Comparer les valeurs des variables des deux programmes en même temps avec les même conditions et débugger à quel moment la formule sur l'arduino est fausse.

## 3. Desktop - GUI

Réaliser un GUI en python pour le projet.

### Problème

Quel méthode de GUI utiliser?

### Solution

PyQt6 pour le GUI.

Qt est un framework graphique (entre autre) très pratique d'utilisation en C++.

Ils ont développé PyQt pour python, qui s'emploie preque pareil (utiliser la documentation de Qt C++ pour PyQt est faisable, cela montre à quel point PyQt est ressemblant à Qt).

Il existe aussi PySide2, qui est une version open source de PyQt, mais il a été décidé d'utiliser PyQt car nous avions peur d'avoir de la peine à utiliser PySide2.

## 4. Desktop - Connection Serial

TODO: LUCA