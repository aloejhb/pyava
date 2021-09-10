import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from .parameter_scan_lattice import load_scan_par

def show_movie(movie):
    fig, ax = plt.subplots()
    ims = []
    for i in range(movie.shape[0]):
        im = plt.imshow(movie[i, :, :], animated=True)
        ims.append([im])
    ani = animation.ArtistAnimation(fig, ims, interval=50, repeat_delay=1000)
    plt.close(fig)
    return ani




def plot_cluster_shape(ax, lat, t_stop=np.inf):
    radius = lat.radius
    extent = [-radius, radius, radius, -radius]
    state_mat = np.multiply(lat.node_type_mat, lat.act_time_mat<=t)
    ax.matshow(state_mat, extent=extent)


def plot_cluster_shape_grid(indir, repeat_nb):
    pass
    # TODO finish this
    # scan_par = load_scan_par(indir)
    # j, k = (17, 19)
    # subdir = os.path.join(indir, 'j_{:03d}_k_{:03d}'.format(j, k))
    # repeat_nb = 29
    # lat = read_lattice(os.path.join(subdir, '{:03d}.pkl'.format(repeat_nb)))

    # t = 300
    # print('{}: {}'.format(par_list[0], mesh1[j]))
    # print('{}: {}'.format(par_list[1], mesh2[k]))
