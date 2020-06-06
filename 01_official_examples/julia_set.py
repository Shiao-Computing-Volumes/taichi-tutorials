import taichi as ti

# ----------------------------------------------------------------------------
# Settings

# N: integer, a global variable, # of pixels
N = 640

# ARCH: processor
ARCH = ti.cpu

# ITER: integer, # of iterations of drawing
ITER = 500

# ----------------------------------------------------------------------------
# Functions

@ti.func
def complex_sqr(z):
    return ti.Vector([z[0]**2 - z[1]**2, z[1] * z[0] * 2])


@ti.kernel
def paint(t: ti.f32):
    for i, j in pixels:  # Parallized over all pixels
        c = ti.Vector([-0.8, ti.cos(t) * 0.2])
        z = ti.Vector([i / N - 1, j / N - 0.5]) * 2
        iterations = 0
        while z.norm() < 20 and iterations < 50:
            z = complex_sqr(z) + c
            iterations += 1
        pixels[i, j] = 1 - iterations * 0.02


# ----------------------------------------------------------------------------
# Main

if __name__ == '__main__':

    ti.init(arch=ARCH)
    gui = ti.GUI("Julia Set", res=(N * 2, N))
    pixels = ti.var(dt=ti.f32, shape=(N * 2, N))

    for i in range(ITER):
        paint(i * 0.03)
        gui.set_image(pixels)
        gui.show()
