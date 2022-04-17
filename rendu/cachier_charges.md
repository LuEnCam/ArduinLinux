# Smardlino CaCha

## Projet

Ce projet a pour but d'interfacer un arduino à un ordinateur

Comme input depuis l'arduino, un joystick est employé
Comme output sur l'arduino, une led rgb est employée


L'idée est depuis le PC de pouvoir changer la couleur de la LED, ainsi que de pouvoir lire les valeurs du joystick.

## Workpackages

### WP 1 - Arduino

Pouvoir exporter un script sur l'arduino, afin de:

- lire les valeurs du joystick
- changer la couleur de la led
- envoyer et recevoir des informations depuis le PC

### WP 2 - PC

Faire un script/application afin de pouvoir envoyer et recevoir des informations sur un port USB

Language choisi: Python

## Répartition du travail

### WP 1

Jarod & Luca:

- comprendre arduino
- lire les valeurs du joystick
- changer la couleur de la led
- envoyer et recevoir des informations depuis le PC avec Serial.print et Serial.read

Jarod:

- conversion depuis un angle en valeur rgb (hsv to rgb)

Luca:

- analyse des valeurs en input côté script arduino

### WP 2

Jarod:

- création d'un GUI

Luca:

- interfacage python-arduino avec pyserial

## Extra

Jarod & Luca:

- sketch arduino only permettant de changer la valeur d'une led avec le joystick connecté

Luca:

- ajout d'un interfacage manette N64 -> arduino (pas implémenté dans la partie finale du projet).
