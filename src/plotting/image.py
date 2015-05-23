"""A plotting module for images"""
import numpy as np
import ipc

images = {}
def plotImage(record, history=10, vmin=None, vmax=None, log=False):
    """Plotting an image.

    Args:
        :record(Record): record.data is plotted as an image

    Kwargs:
        :history(int):  Length of history buffer
        :vmin(float):   Minimum value
        :vmax(float):   Maximum value
        :log(boolean):  Plot image in log scale (needs restart of GUI, only works with grayscale colormap)
    """
    if record is None:
        return
    if(not record.name in images):
        ipc.broadcast.init_data(record.name, data_type='image', history_length=history, vmin=vmin, vmax=vmax, log=log)
        images[record.name] = True
    image = record.data
    sh = image.shape
    if (image.ndim == 3):
        image = image.reshape(sh[0]*sh[2], sh[1])
    ipc.new_data(record.name, image)