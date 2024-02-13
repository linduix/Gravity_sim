import moderngl_window as mglw


class App(mglw.WindowConfig):
    window_size = 1600, 900
    resource_dir = 'test_shaders'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.quad = mglw.geometry.quad_fs()
        self.prog = self.load_program(vertex_shader='vertex_shader.glsl',
                                      fragment_shader='fragment_shader.glsl')
        self.set_uniform('resolution', self.window_size)
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
        print(f'mouse down {dx} {dy}')

    def mouse_position_event(self, x: int, y: int, dx: float, dy: float):
        self.mouse_position(x, y)
        print('mouse up')

    def render(self, time: float, frame_time: float):
        self.ctx.clear()
        self.set_uniform('time', time)
        self.set_uniform('mouse', self.mouse_pos)
        self.quad.render(self.prog)


if __name__ == '__main__':
    mglw.run_window_config(App)
