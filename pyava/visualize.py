import matplotlib.pyplot as plt
import matplotlib.animation as animation


def show_movie(movie):
    fig, ax = plt.subplots()
    ims = []
    for i in range(movie.shape[0]):
        im = plt.imshow(movie[i, :, :], animated=True)
        ims.append([im])
    ani = animation.ArtistAnimation(fig, ims, interval=50, repeat_delay=1000)
    plt.close(fig)
    return ani
