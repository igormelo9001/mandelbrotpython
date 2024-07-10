import numpy as np
import matplotlib.pyplot as plt
import imageio

def mandelbrot(c, max_iter):
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter):
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty((width, height))
    for i in range(width):
        for j in range(height):
            n3[i, j] = mandelbrot(r1[i] + 1j*r2[j], max_iter)
    return (r1, r2, n3)

def save_frame(xmin, xmax, ymin, ymax, width, height, max_iter, filename):
    dpi = 80
    img_width = dpi * width
    img_height = dpi * height
    r1, r2, n3 = mandelbrot_set(xmin, xmax, ymin, ymax, img_width, img_height, max_iter)

    plt.figure(dpi=dpi, figsize=(width, height))
    plt.imshow(n3.T, extent=[xmin, xmax, ymin, ymax], cmap='hot')
    plt.xlabel("Re(c)")
    plt.ylabel("Im(c)")
    plt.savefig(filename)
    plt.close()

def create_zoom_animation(x_center, y_center, zoom_start, zoom_end, zoom_steps, width=10, height=10, max_iter=256):
    filenames = []
    for i in range(zoom_steps):
        zoom = zoom_start * (zoom_end / zoom_start) ** (i / zoom_steps)
        xmin = x_center - zoom
        xmax = x_center + zoom
        ymin = y_center - zoom
        ymax = y_center + zoom
        filename = f"frame_{i:03d}.png"
        save_frame(xmin, xmax, ymin, ymax, width, height, max_iter, filename)
        filenames.append(filename)
    
    # Create the GIF
    with imageio.get_writer('mandelbrot_zoom.gif', mode='I', duration=0.1) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)

    # Optionally, remove the files after creating the GIF
    for filename in filenames:
        os.remove(filename)

# Example usage
create_zoom_animation(x_center=-0.75, y_center=0.0, zoom_start=1.5, zoom_end=0.001, zoom_steps=50)
