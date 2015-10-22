#Relion code repository

- [Plotting euler angle distributions for 3D reconstructions] (https://github.com/leschzinerlab/Relion#plotting-euler-angle-distributions-for-3d-reconstructions)
- Removing over-represented views within Relion STAR files
- Converting CTFFIND3 outputs into Relion format

##Plotting euler angle distributions for 3D reconstructions

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

##Removing over-represented views within Relion STAR files

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
  --AngleRotLim1=INT   Lower limit for AngleRot. (Default=-180)
  --AngleRotLim2=INT   Upper limit for AngleRot. (Default=180)
  --AngleTiltLim1=INT  Lower limit for AngleTilt. (Default=0)
  --AngleTiltLim2=INT  Upper limit for AngleTilt. (Default=180)
  --AnglePsiLim1=INT   Lower limit for AnglePsi. (Default=-180)
  --AnglePsiLim2=INT   Upper limit for AnglePsi. (Default=180
  --savetemp           Flag to save list of particles removed from original
                       stack.
  -d                   debug
  ```
###Usage
By default, if no euler angle limits are specified, this program will not remove any particles from the .star file.

In order to remove particles from within a euler angle range, you must specify the lower and upper limits from which the particles will be excluded.

For flexibility, the program can 1) remove particles from the same input file, or 2) remove particles from a different file. And, the list of particles that were excluded can be saved by specifying the *--savetemp* option.

###Example
For example, if I have an over-represented euler angle range of 50 - 80 degrees from the AngleRot angle and I know that I want to remove 10,000 particles from this range in order to restore it to the baseline distribution:

```
$ Relion/reweight_particle_stack.py  --stareuler=relion_data.star --starparticle=relion_data.star --AngleTiltLim1=50 --AngleTiltLim2=80 --savetemp
```
* Where, *relion_data.star* is a data file from relion that will have certain particles removed. And, the particles removed will be saved, and stored in a new file named *relion_data_particlesRemoved.star*.
