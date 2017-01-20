### Installation

- Setup environment

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

- Download the data

```
mkdir data
mkdir images
```

Download the file into the `data` folder

Then run the program :

```
python run.py
```

The output will be the number of cluster found at each second, and the event json at every change.

If you change the value of the variable `PLOT` in `run.py`, you will have the plot of each step (with colored clusters) in the folder `images`.

- IPython Notebook

You can browse the file `exploration.ipynb` which explain the choice of some variables. (PS: The first graph doesn't seem to work)

### Main goal

The main goal of this project is to detect groups creation/modification/deletion on temporal and geo-spatial data.

### Problematics

 - Accuracy of the data
    - Distance metric
    - Shape computation
    - Centroid localization
 - Sampling of the data
    - Handle time series with beg gaps (cut in multiple part)
    - Predict the short term position when the gap is reasonable
 - 'Exclusive' clustering without `k`

### Approach

#### Sampling and accuracy

 - Discard of the outlier
   - Accuracy > 60m
   - Series with elapsed time > 1min
 - Linear interpolation of the position

#### Clustering

Unsupervised algorithm to cluster people based on their closeness :

 - We do not want to put everyone in a cluster
 - The cluster must be very dense
 - The number of k can change each second.

Distance metric :

 - What distance is reasonnable Haversine

### Results

#### Parameters

 - Screens
 -

### To be done

 - Check the last minute and discard group adding or creation if the point is not in this group.
 - `tests` folder with unit tests

### Future work

#### Data exploration

 - Trajectories : the density of the accuracy circle could be higher in the point 'global' direction. It would change the distance computation. We could use the Ramer-Douglas-Peucker algorithm to extract the general path of the point.

#### Contextual informations

 - Meeting points
 - Rivers
 - Museum ...

#### Graphical

 - Add circle of the size of the accuracy with a corresponding `alpha`
 - Add the map of Paris

### Bibliography

`Density-based Place Clustering in Geo-Social Networks`




 - Aire de la sphere toujours égale à 1 (densité en fonction du rayon)
   - Aire pondérer dans la direction de la personne
 - Calcul de la densité des intersections
 - Approximer lat et long pour etre dans un plan


 - Visualisation avec couleur

 - Premiere regle bateau

 - Et après faire un algo qui prend en compte les corrections

 Donnée polaire ton euler



On filtre tous les points dont l'accuracy est supérieur à 65m ~= 25% de la base
On prend les users qui n'ont aucun elasped time > 1min ~= 81% de la base


Probleme de serie qui s'arrete
Interpolation


Conserver l'information user:time:cluster et ne le valider que si le tps total est > Epsilon


Algorithm choice :

 - clustering
 - no information on k
 - density oriented
 - distance from centroide

Distance : Euclidean seems ok but used Haversine to be able to scale up



Create folder data
Create folder images


Ajout d'un proba sur le calcul de distance