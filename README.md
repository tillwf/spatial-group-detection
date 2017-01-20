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

The output will be the number of cluster found at each second, and the event (json format) at every change.

Example

```jso
{
    'type': 'decrease',
    'date': 2,
    'centroid': (1.0, 1.0),
    'people_out': set([17]),
    'previous_cluster_id': 15,
    'cluster_id': 16,
    'population': set([16, 15]),
    'density': 0.0
}
```

If you change the value of the variable `PLOT` in `run.py`, you will have the plot of each step (with colored clusters) in the folder `images`.

- IPython Notebook

You can browse the file `exploration.ipynb` which explain the choice of some variables. (PS: The first graph doesn't seem to work)

### Main goal

The main goal of this project is to detect groups creation/modification/deletion on temporal and geo-spatial data.

### Problematics

#### The Accuracy of the data

Each position comes with an accuracy which can be very low (high value in meters of imprecision). We then face multiple problems :

    - Distance metric
    - Shape computation
    - Centroid localization

#### The sampling of the data

The series of points for a user is not regularly sampled and like the accuracy there can be long moment (many hours) between two points. We have to :

    - Handle time series with big gaps (cut in multiple part)
    - Predict the short term position when the gap is reasonable (we can use the information of the past trajectory)

#### The clustering

The main problem is to group people without knowing the number of group. We have to use the repartition of the point to extract this information.

### Approach

#### Sampling and accuracy

 - Discard the outliers
   - Using the `exploration.ipynb`, we chose 60m as a minimum viable accuracy
   - We also removed series with elapsed time > 1min

 - Stationary interpolation of the position if the last position was less than 1 minute before

With this interpolation, we can re-use the series we removed earlier : if no point was detected for 1 minute, the algorithm will not consider it.

#### Clustering

Unsupervised algorithm to cluster people based on their closeness :

 - We do not want to put everyone in a cluster
 - The cluster must be very dense
 - The number of k can change each second

We used the DBSCAN for multiple reason and mainly for its weaknesses :
 - Handle only regularly dense clusters
 - Comes with the parameter `epsilon` which defines the maximum distance between two samples

Distance metric :

  - First the Haversine distance between the two points
  - Then if the accuracy was very low, we weighted it by using the max and min distances possible between points

### Results

#### Parameters

The only parameters would be the accuracy filter and the epsilon of DBSCAN. The latter is easy to choose when there are no accuracy problems : because we used the Haversine distance, we can reasonably select a minimum distance between two people in the same groups (for instance 4 meters). With the accuracy, we chose 50 meters empirically.

#### Screenshot

Here is an example of an event ()

### To be done

 - Check the last minute and discard group adding or creation if the point is not in this group.
 - Bug fixing / Refacto

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
