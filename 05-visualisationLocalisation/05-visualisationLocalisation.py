import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Dimensions de la pièce A MODIFIER
longueur = 10  # en mètres
largeur = 5    # en mètres



#Distance entre le capteur et les bornes
#A RECUPERER DANS UNE BDD
rayonCIEL1 = 5.5
rayonCIEL2 = 2.7
rayonCIEL3 = 5.5 
# Coordonnées des balises A MODIFIER
points = [(0, 0, rayonCIEL1), (5, 5, rayonCIEL2), (10, 0, rayonCIEL3)]

fig, ax = plt.subplots()
# Dessin pièce
ax.add_patch(patches.Rectangle((0, 0), longueur, largeur, edgecolor='black', facecolor='lightgrey'))


# Placement des bornes Wifi
borneNum = 0
for x, y, rayon in points:
    ax.plot(x, y, 'ro')  #en rouge
    ax.text(x + 0.2, y + 0.2, f'Borne {borneNum }', color='red', fontsize=8)
    borneNum = borneNum +1


#Ajout de la distance du capteur autour de la borne modélisé par de cercles 
for x, y, rayon in points:
    circle = patches.Circle((x, y), rayon, edgecolor='blue', facecolor='none', linestyle='--')
    ax.add_patch(circle)

# Ajuster les axes pour bien voir le graphique
ax.set_xlim(-1, longueur + 1)
ax.set_ylim(-1, largeur + 1)
ax.set_aspect('equal')
ax.grid("on")
# Ajouter des labels et un titre
plt.xlabel('Longueur (mètres)')
plt.ylabel('Largeur (mètres)')
plt.title('Simulation de la pièce')

# Afficher le graphique
plt.show()
