import sys
import os
import datetime
import numpy as np
sys.path.append('..')
import pyava
import pyava.parameter_scan_lattice as psc


run_func = psc.run_ei_perc_2d
tstep = 200
par_list = ['p', 'p_exc']
step_size = 0.05
mesh1 = np.arange(0, 1+step_size, step_size)
mesh2 = np.arange(0, 1+step_size, step_size)
print(mesh1)
print(mesh2)
mesh_list = [mesh1, mesh2]
fixed_par = dict(tstep=tstep, nb_repeats=30)
out_root_dir = '../results'
fmt='%Y-%m-%d-%H-%M-%S'
timestamp = datetime.datetime.now().strftime(fmt)
outdir = os.path.join(out_root_dir, timestamp)
if not os.path.exists(outdir):
    os.mkdir(outdir)
psc.parameter_scan(par_list, mesh_list, fixed_par, run_func,
                   outdir=outdir, seed=21, parallel=True)
