import moderngl_window as mglw
import moderngl_window as mglw
from gravutils import Body


class App(mglw.WindowConfig):
    window_size = 1600, 900
    resource_dir = 'shaders'
    body1 = Body(800, 20, (500, 500), (0.0000, 0.000003))
    body2 = Body(800, 20, (1000, 500), (0.0000, -0.000003))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.quad = mglw.geometry.quad_fs()
        self.prog = self.load_program(vertex_shader='vertex_shader.glsl',
                                      fragment_shader='fragment_shader.glsl')
        self.set_uniform('resolution', self.window_size)

        self.set_uniform('b1r', self.body1.r)
        self.set_uniform('b1m', self.body1.mass)

        self.set_uniform('b2r', self.body2.r)
        self.set_uniform('b2m', self.body2.mass)
        # self.window_size = kwargs['window']
        self.mouse_pos = (0, 0)

    def set_uniform(self, u_name, u_value):
        try:
            self.prog[u_name] = u_value
        except KeyError:
            print(f'uniform: {u_name}, - not used in shader')

    def mouse_position(self, x, y):
        # Update mouse position
        self.mouse_pos = (x, self.window_size[1]-y)  # Convert to OpenGL coordinate system
        # print(f"Mouse position: {self.mouse_pos}")


    def mouse_drag_event(self, x: int, y: int, dx: int, dy: int):
        self.mouse_position(x, y)

    def mouse_position_event(self, x: int, y: int, dx: float, dy: float):
        self.mouse_position(x, y)

    def render(self, time: float, frame_time: float):
        self.ctx.clear()

        self.body1.calc(self.body2, frame_time, self.window_size)
        self.body2.calc(self.body1, frame_time, self.window_size)

        self.body1.update(frame_time)
        self.body2.update(frame_time)

        self.set_uniform('b1pos', self.body1.pos)
        self.set_uniform('b2pos', self.body2.pos)
        # self.set_uniform('time', time)
        # self.set_uniform('mouse', self.mouse_pos)
        self.quad.render(self.prog)


if __name__ == '__main__':
    mglw.run_window_config(App)
