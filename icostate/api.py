# -- Imports ------------------------------------------------------------------

from icotronic.can import Connection

# -- Classes ------------------------------------------------------------------


class ICOSystem:
    def __init__(self):
        self.connection = Connection()
