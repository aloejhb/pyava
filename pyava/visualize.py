import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from .parameter_scan_lattice import load_scan_par
from .graphio import read_lattice


def show_movie(movie):
    fig, ax = plt.subplots()
    ims = []
    for i in range(movie.shape[0]):
        im = ax.matshow(movie[i, :, :], cmap='RdYlBu', animated=True)
        im.set_clim([-1, 1])
        ims.append([im])
    ani = animation.ArtistAnimation(fig, ims, interval=50, repeat_delay=1000)
    plt.close(fig)
    return ani


def plot_cluster_shape(ax, lat, t_stop):
    radius = lat.radius
    extent = [-radius, radius, radius, -radius]
    state_mat = np.multiply(lat.node_type_mat, lat.act_time_mat<=t_stop)
    im = ax.matshow(state_mat, extent=extent, cmap='RdYlBu')
    im.set_clim([-1, 1])


def plot_cluster_shape_grid(indir, repeat_nb, gstep=[1,1], grange=[(0,1),(0,1)], t_stop=np.inf):
    scan_par = load_scan_par(indir)

    mesh_list = np.array(scan_par['mesh_list'])
    mesh0 = mesh_list[0][(mesh_list[0] >= grange[0][0]) & (mesh_list[0] <= grange[0][1])]
    mesh1 = mesh_list[1][(mesh_list[1] >= grange[1][0]) & (mesh_list[1] <= grange[1][1])]
    m0 = mesh0[::gstep[0]]
    m1 = mesh1[::gstep[1]]
    print(m0)
    print(m1)
    fig, axs = plt.subplots(len(m0), len(m1), figsize=(11, 11),
                            sharey=True, sharex=True)
    for j_idx in range(len(m0)):
        for k_idx in range(len(m1)):
            j = list(mesh_list[0]).index(m0[j_idx])
            k = list(mesh_list[1]).index(m1[k_idx])
            print((j,k))
            subdir = os.path.join(indir, 'j_{:03d}_k_{:03d}'.format(j, k))
            lat = read_lattice(os.path.join(subdir, '{:03d}.pkl'.format(repeat_nb)))
            ax = axs[k_idx][j_idx]
            plot_cluster_shape(ax, lat, t_stop)
            ax.tick_params(axis='both', which='both',
                           bottom=False, labeltop=False,
                           top=False, left=False, labelleft=False)
            if j_idx == 0:
                ax.set_ylabel('{:.2f}'.format(mesh_list[1][k]))
            if k_idx == len(m1)-1:
                ax.set_xlabel('{:.2f}'.format(mesh_list[0][j]))
            #     ax.tick_params(axis='y', labelsize=5)
            # else:
            #     ax.tick_params(axis='y', left=False)
            # ax.tick_params(axis='x', bottom=False, top=False)
            # if j_idx == len(m0)-1:
            #     ax.tick_params(axis='x', bottom=True, labeltop=False,
            #                    labelbottom=True, labelsize=5)

    par_list = scan_par['par_list']
    fig.supxlabel(par_list[0])
    fig.supylabel(par_list[1])
    return fig


def activation_movie(lat, tmax=None):
    if tmax is None:
        tmax = lat.act_time_mat[lat.act_time_mat<1e308].max().astype('int')
    movie = np.zeros((tmax, lat.act_time_mat.shape[0], lat.act_time_mat.shape[1]))
    for t in range(tmax):
        movie[t,:,:] = np.multiply(lat.node_type_mat, lat.act_time_mat<=t+1)
    return movie
