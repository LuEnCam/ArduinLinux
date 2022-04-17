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
- prendre la "distance du joystick par rapprot à son centre" comme valeur de saturation.

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

Depuis le script python, des énénements sont déclenchés afin de communiquer avec l'arduino (appui d'un bouton, changement des valeurs des barres glissantes pour controller la saturation et la couleur, allumer ou éteindre la LED).
Tous les événements sont connectés à la même fonction :
```python
	def send_input(ser: serial, _input: str): 
```
**serial** correspond à l'objet établissant la communication avec l'arduino tandis que **_input** correspond à la commande envoyée à l'arduino. La commande envoyée est toujours de la forme suivante:
 ```python
	## _input = on_off hue intensity mode 
```
**on_off** correspond à un entier (1 pour allumé, 0 pour éteindre)
**hue** correspond à la valeur en entier de la couleur sur le cercle HUE (entre 0 et 359)
**intensity** correspond à la valeur en float de l'intensité de la couleur (0.0 pour blanc et 1.0 pour la couleur vive)
**mode** correspond au mode de contrôle de la LED en entier (1 pour le mode "joystick" et 2 pour le mode "UI")

Exemple: 
```python
_input = "1 120 1.0 2" ## ceci envoie l'information que la led est allumée, sur l'angle de couleur 120, avec une intensité de 1.0 et en mode UI
```

Avant de pouvoir controller l'arduino avec le GUI, il est nécessaire de faire l'interfaçage entre le script python et l'arduino. Dans le GUI, un champ est mis à disposition pour spécifier le port sur lequel est connecté l'arduino (que ce soit sur windows ou Linux). La librairie python **serial.tools** permet d'identifier les ports disponibles où se trouvent les périphériques branchés à la machine:

![](../images/Capture5.png)

Exemple sur Windows : 

![](../images/Capture6.png)

Exemple sur Linux : 

![](../images/Capture7.png)

Lorsque le mode joystick est activé, seul le changement de mode côté GUI est disponible (il n'est pas possible de modifier les valeurs de la LED sur l'UI pendant le mode Joystick).

## 5. Lecture des valeurs du joysitck

TODO Jarod

