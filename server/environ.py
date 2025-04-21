import os

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), '.env')

class Env:
    """ Simple environ """

    def __init__(self, env_file=None):
        
        if not env_file and os.path.exists(DEFAULT_PATH):
            env_file = DEFAULT_PATH
        
        if env_file:
            self.read_env(env_file)

        self.environ = {
            **os.environ,
            **getattr(self, 'environ', {})
        }

    def read_env(self, path):
        with open(path, 'r') as f:
            self.environ = dict(
                (lambda l: [l[0], l[1].strip('"')])(
                    line.replace('\n', '').split('=', maxsplit=1)
                )
                for line in f.readlines() if not line.startswith('#')
            )

    def __call__(self, var, default=None):
        return self.get(var, default)

    def get(self, var, default=None):
        return self.environ.get(var, default)

    def str(self, var, default=None):
        return str(self.get(var, default))

    def bool(self, var, default=None):
        value = self.get(var, default)
        OK_VALUES = ('true', 'on', 'ok', 'y', 'yes', '1')
        return bool(value) and value.lower().strip() in OK_VALUES
