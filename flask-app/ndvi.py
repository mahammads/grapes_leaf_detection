import warnings
from cv2 import CV_32SC3
warnings.filterwarnings('ignore')
import numpy as np
from matplotlib import pyplot as plt  # For image viewing
import cv2
import os
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import ticker
from matplotlib.colors import LinearSegmentedColormap
from pathlib import Path
# Load image and convert to float - for later division

def ndvi(img_path):
    d=  os.listdir(img_path)
    image=cv2.imread(os.path.join(img_path,d[0]))
    im = image.astype(np.float)
    ir = (image[:,:,0]).astype('float')

    # Get one of the IR image bands (all bands should be same)
    #blue = image[:, :, 2]

    #r = np.asarray(blue, float)

    r = (image[:,:,2]).astype('float')

    # Create a numpy matrix of zeros to hold the calculated NDVI values for each pixel
    ndvi = np.zeros(r.size)  # The NDVI image will be the same size as the input image

    # Calculate NDVI
    ndvi = np.true_divide(np.subtract(ir, r), np.add(ir, r))

    # Display the results
   

    #a nice selection of grayscale colour palettes
    cols1 = ['blue', 'green', 'yellow', 'red']
    cols2 =  ['gray', 'gray', 'red', 'yellow', 'green']
    cols3 = ['gray', 'blue', 'green', 'yellow', 'red']

    cols4 = ['black', 'gray', 'blue', 'green', 'yellow', 'red']

    def create_colormap(args):
        return LinearSegmentedColormap.from_list(name='custom1', colors=cols3)
    #colour bar to match grayscale units
    def create_colorbar(fig, image):
            position = fig.add_axes([0.125, 0.19, 0.2, 0.05])
            norm = colors.Normalize(vmin=-1., vmax=1.)
            cbar = plt.colorbar(image,
                                cax=position,
                                orientation='horizontal',
                                norm=norm)
            cbar.ax.tick_params(labelsize=6)
            tick_locator = ticker.MaxNLocator(nbins=3)
            cbar.locator = tick_locator
            cbar.update_ticks()
            cbar.set_label("NDVI", fontsize=10, x=0.5, y=0.5, labelpad=-25)

    fig, ax = plt.subplots()
    image = ax.imshow(ndvi, cmap=create_colormap(colors))

    plt.axis('off')

    create_colorbar(fig, image)

    extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())

    return fig,extent

if __name__ == "__main__":
    # gray_path = Path(os.getcwd()+"/app/static/uploads/")
    # output_name = 'app/static/uploads/InfraBl.jpg'
    # fig,extent =  ndvi(gray_path)
    # fig.savefig(output_name, dpi=600, transparent=True, bbox_inches=extent, pad_inches=0)
  pass

