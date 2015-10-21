#Relion code repository

- Plotting euler angle distributions for 3D reconstructions
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
