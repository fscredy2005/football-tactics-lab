# ⚽ Football Tactics Lab — Argentine × France, finale 2022

Application de visualisation tactique gratuite, avec cartes de passes et de tirs, xG, sélections équipe/joueur/période et exports CSV/PNG.

## Publier sur GitHub puis Streamlit Community Cloud

1. Télécharge le ZIP fourni et **décompresse-le** sur ton ordinateur.
2. Ouvre **https://github.com/new**, crée un dépôt `football-tactics-lab`, puis choisis `Public` si tu souhaites que tout le monde puisse accéder à l'application.
3. Dans ce nouveau dépôt, clique sur **Add file → Upload files**. Glisse les fichiers de ce dossier (à la racine du dépôt), en particulier :
   - `streamlit_app.py`
   - `football_tactics_lab.html`
   - `requirements.txt`
   - `README.md`
   - `statsbomb_logo.png` (logo officiel inclus)
4. Valide avec **Commit changes**.
5. Ouvre **https://share.streamlit.io/**. Connecte GitHub si nécessaire, puis **Create app → Yup, I have an app**.
6. Sélectionne le dépôt `football-tactics-lab`, la branche `main` et le fichier principal `streamlit_app.py`.
7. Choisis éventuellement un sous-domaine puis **Deploy**.
8. Une fois publié, teste **Passes / Tirs**, le filtre **Joueur**, le chargement StatsBomb, **Exporter PNG** et l’affichage du logo StatsBomb au-dessus du tableau de bord.

Les mises à jour du dépôt sont ensuite redéployées automatiquement par Streamlit.

## Données et fonctionnement

- Match StatsBomb : `3869685` — finale Argentine–France, 18 décembre 2022.
- URL officielle : https://raw.githubusercontent.com/hudl/open-data/master/data/events/3869685.json
- Au lancement, Streamlit essaie de récupérer le fichier public depuis GitHub et de le conserver en cache pendant six heures.
- Si cette récupération échoue, le JavaScript tente un chargement direct depuis le navigateur.
- Si les deux méthodes échouent, clique sur **Importer un JSON** et importe le fichier `3869685.json` depuis ton ordinateur.
- Aucun événement fictif n'est substitué aux données du match. Les cartes restent en attente en cas d'erreur de chargement.
- Une sélection de matchs StatsBomb peut être importée manuellement, mais les analyses narratives du Mondial 2022 restent spécifiques à cette rencontre.

## Coût / besoins techniques

- Le code utilise uniquement Python standard et Streamlit ; aucun compte/API privée StatsBomb et aucune clé de paiement.
- GitHub et Streamlit Community Cloud proposent un usage gratuit avec limitations et politiques de service.
- Exécuter localement (si Python/Streamlit sont installés) : `pip install -r requirements.txt`, puis `streamlit run streamlit_app.py`.

## Attribution et publication — important

**StatsBomb Open Data** : https://github.com/hudl/open-data

Le dépôt StatsBomb demande, pour une analyse publiée, de **mentionner StatsBomb comme source et d'utiliser son logo**. Le fichier `statsbomb_logo.png` **est inclus dans ce ZIP**. Il est dérivé, sans modification de forme ni de couleur, du logo vectoriel publié par Hudl dans son dépôt de ressources publiques :

- [Logo original officiel Hudl (SVG)](https://github.com/hudl/public-images/blob/master/SB%20-%20Core%20Wordmark%20-%20Colour%20positive.svg)
- [Données StatsBomb Open Data et conditions d'attribution](https://github.com/hudl/open-data)

L'ancien [lien « Media Pack »](https://statsbomb.com/media-pack/) redirige désormais vers une page produit. Il existe [une question publique non résolue](https://github.com/hudl/open-data/issues/80) sur le logo exact à privilégier depuis le changement d'identité de marque. Si tu prévois une exploitation commerciale, confirme les directives actuelles auprès de Hudl/StatsBomb.

Cette application est une démonstration pédagogique indépendante, sans affiliation à Hudl ou StatsBomb.
