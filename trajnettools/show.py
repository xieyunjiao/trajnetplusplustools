from collections import defaultdict
from contextlib import contextmanager

import matplotlib.pyplot as plt


@contextmanager
def canvas(image_file=None, **kwargs):
    """Generic matplotlib context."""
    fig, ax = plt.subplots(**kwargs)

    yield ax

    fig.set_tight_layout(True)
    if image_file:
        fig.savefig(image_file, dpi=300)
    fig.show()
    plt.close(fig)


@contextmanager
def paths(input_paths, output_file=None):
    """Context to plot paths."""
    primary_pedestrian = input_paths[0][0].pedestrian
    input_rows = [row for path in input_paths for row in path]
    with rows(primary_pedestrian, input_rows, output_file) as ax:
        yield ax


@contextmanager
def rows(primary_pedestrian, input_rows, output_file=None):
    """Context to plot rows."""
    trajectories_by_id = defaultdict(list)
    for row in input_rows:
        trajectories_by_id[row.pedestrian].append(row)

    with canvas(output_file, figsize=(8, 8)) as ax:
        ax.grid(linestyle='dotted')
        ax.set_aspect(1.0, 'datalim')
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')

        yield ax

        # primary
        xs = [r.x for r in trajectories_by_id[primary_pedestrian]]
        ys = [r.y for r in trajectories_by_id[primary_pedestrian]]
        # track
        ax.plot(xs, ys, color='black', linestyle='solid', label='primary')
        # markers
        ax.plot(xs[0:1], ys[0:1], color='black', marker='x', label='start', linestyle='None')
        ax.plot(xs[-1:], ys[-1:], color='black', marker='o', label='end', linestyle='None')

        # other tracks
        for ped_id, ped_rows in trajectories_by_id.items():
            if ped_id == primary_pedestrian:
                continue

            xs = [r.x for r in ped_rows]
            ys = [r.y for r in ped_rows]
            # markers
            ax.plot(xs[0:1], ys[0:1], color='black', marker='x', linestyle='None')
            ax.plot(xs[-1:], ys[-1:], color='black', marker='o', linestyle='None')
            # track
            ax.plot(xs, ys, color='black', linestyle='dotted')

        # frame
        ax.legend()