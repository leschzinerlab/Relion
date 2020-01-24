# RELION code repository


## Plotting euler angle distributions for 3D reconstructions

Given an output *.star* file from Relion, you can visualize the euler angles by opening the .bild file with UCSF Chimera.

Alternatively, if you would like to generate 1D histogram plots for any euler angle, or a 2D heat-map of two specific euler angles, you can use *plot_indivEuler_histogram_fromStarFile.py*:
```
$ Relion/plot_indivEuler_histogram_fromStarFile.py
Usage: plot_indivEuler_histogram_fromStarFile.py --starfile=<relion_star_file>

Options:
  -h, --help         show this help message and exit
  --starfile=FILE    Relion star file (data.star)
  --rlnEuler=STRING  Name of Relion euler angle designation:
                     AngleRot,AngleTilt, AnglePsi. Provide two angle names
                     (e.g. AngleRot,AngleTilt) for a 2D heat map of euler
                     angles
  --binsize=INT      Optional: bin size for histogram of euler angles
                     (Default=5)
  -d                 debug
```

This script uses numpy and matplotlib to generate 1D/2D histograms for the specified euler angle (AngleRot, AngleTilt, AnglePsi) that is within the Relion .star file.

### Example output images

**1D histogram for a given euler angle**

![alt tag](https://github.com/leschzinerlab/Relion/blob/master/plot_indivEuler_histogram_fromStarFile_1Dhist.png)

**2D histogram for a given euler angle**

![alt tag](https://github.com/leschzinerlab/Relion/blob/master/plot_indivEuler_histogram_fromStarFile_2Dhist.png)

## Removing over-represented views within Relion STAR files

After visualizing the above results for euler angle distributions within your data, the following script will randomly remove a specific subset of particles within a specified euler angle range, thus reweighting the euler angle distribution for your data.

```
$ Relion/reweight_particle_stack.py
Usage: reweight_particle_stack.py --stareuler=<relion_star_file> --starparticle=<relion_star_file> [lims]

Options:
  -h, --help           show this help message and exit
  --stareuler=FILE     Output Relion star from refinement/classification
                       containing euler angles
  --starparticle=FILE  Relion star file that will be reweighted based upon
                       euler angles.
  --remove=INT         Number of particles to remove from preferential view,
                       specified WITHIN the limits below
  --AngleRotLim1=INT   Lower limit for AngleRot.
  --AngleRotLim2=INT   Upper limit for AngleRot.
  --AngleTiltLim1=INT  Lower limit for AngleTilt.
  --AngleTiltLim2=INT  Upper limit for AngleTilt.
  --AnglePsiLim1=INT   Lower limit for AnglePsi.
  --AnglePsiLim2=INT   Upper limit for AnglePsi.
  --saveremoved        Flag to save list of particle numbers removed from
                       original list.
  -d                   debug
  ```
### Usage
By default, if no euler angle limits are specified, this program will not remove any particles from the .star file.

In order to remove particles from within a euler angle range, you must specify a range WITHIN euler angles limits that will be removed. For instance, if you wanted to remove particles within the AngleRot range 50 to 90 degrees, you would have these input options:

<pre>--AngleRotLim1=50
--AngleRotLim2=90</pre>

For flexibility, the program can 1) remove particles from the same input file, or 2) remove particles from a different file. And, the list of particles that were excluded can be saved by specifying the *--saveremoved* option.

### Example
For example, if I have an over-represented euler angle range of 50 - 90 degrees from the AngleRot angle and I know that I want to remove 10,000 particles from this range in order to restore it to the baseline distribution:

```
$ Relion/reweight_particle_stack.py  --stareuler=relion_data.star --starparticle=relion_data.star --remove=10000 --AngleTiltLim1=50 --AngleTiltLim2=8=90 --saveremoved
```
* Where, *relion_data.star* is a data file from relion that will have certain particles removed. And, the particles removed will be saved, and stored in a new file named *relion_data_particlesRemoved.txt*.
