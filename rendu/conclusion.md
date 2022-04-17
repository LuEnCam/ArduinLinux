# Conclusion Smardlino

## Ce qui fonctionne

- La modification de la led RGB depuis l'application et le joystick.
- La lecture de l'input du joystick.

## Ce qui ne fonctionne pas

- La connection simultanée du joystick et de la led RGB (pouvoir lire et écrire). Une séparartion entre les deux modes a été nécessaire.
  C'est surement du à une limitation de notre script arduino (peut-être utiliser du multi-threading ?).
