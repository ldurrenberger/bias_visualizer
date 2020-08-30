import bias
import os
import numpy as np
from datetime import datetime

# define constants used
# lo_cutoff: lower range of cutoff value we want to do everything on.
#               Will slice based on average score
# lo_cutoff = 3

# hi_cutoff: higher range of cutoff value we want to do everything on.
#               Will slice based on average score
# hi_cutoff = 3.5

# to_refresh: should program use Google API keys to refresh the data from the spreadsheet?
to_refresh = False

# produce_est: should program output predictions as a csv in new directory?
produce_est = True

# produce_plots: should program output plots as a png in new directory?
produce_plots = True

# show_plots: should program show plots as they are created?
show_plots = False

# https://thispointer.com/python-how-to-get-current-date-and-time-or-timestamp/
date_time_obj = datetime.now()

# https://stackabuse.com/creating-and-deleting-directories-with-python/
# define the name of the directory to be created
path = os.getcwd() + "/est_" + str(date_time_obj.hour) + "_" + str(date_time_obj.minute) + "/"

try:
    os.mkdir(path)
    os.mkdir(path + "/csv")
    os.mkdir(path + "/png")
except OSError:
    print("Creation of the directory %s failed" % path)
else:
    print("Successfully created the directory %s " % path)

for x in np.arange(1.0, 5, .5):
    bias.determine_bias(path, x, x + .5, to_refresh, produce_est, produce_plots, show_plots)
