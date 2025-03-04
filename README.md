# Gangsta Paradise Automation Script

## Description
Ce script automatise des interactions avec l'interface Web de Ganging ITX ou l'application iTX Desktop. Il utilise Selenium pour manipuler un navigateur Web, ainsi que la bibliothèque `pynput` pour intercepter des pressions de touches spécifiques et déclencher des actions automatisées.

## Fonctionnalités
- Ouvre et authentifie un navigateur Chrome pour interagir avec une page Web spécifique.
- Intercepte des pressions de touches et exécute des actions associées.
- Manipule la fenêtre de l'application iTX Desktop.
- Simule des clics de souris et des raccourcis clavier.
- Enregistre les événements et erreurs dans un fichier journal (`gangsta_log`).

## Prérequis
Assurez-vous d'avoir un chromedrive.exe compatible avec votre version de Chrome.

Le script nécessite également un fichier `__config__.xml` dans son répertoire d'exécution contenant le point de contrôle actif.

## Configuration
Le mot de passe `itx_password` est récupéré depuis la variable d'environnement `itx_pwd`. Assurez-vous de le définir avant d'exécuter le script.


## Utilisation
1. Lancez l'exe.
2. Il ouvre automatiquement Chrome et se connecte avec les informations fournies.
3. Il attend les pressions de touches suivantes pour exécuter des actions spécifiques :
   - `ALT + F13` : Met iTX Desktop au premier plan.
   - `ALT + F14` : Met la page Web au premier plan.
   - `ALT + F15` : Exécute une action de "Take Next" selon la fenêtre active.
4. Pour arrêter le script, fermez-le manuellement ou terminez le processus Python.

## Journalisation
Le script génère un fichier journal dans `gangsta_log/` avec les événements et erreurs pour faciliter le débogage.

## Avertissement
- Ce script modifie automatiquement l'état de certaines applications. Assurez-vous de l'utiliser dans un environnement contrôlé.
- Vérifiez toujours les logs en cas de comportement inattendu.

