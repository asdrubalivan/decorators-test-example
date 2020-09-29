from unittest import TestCase
from unittest.mock import patch, Mock
import app
import importlib


class MyTests(TestCase):
    def setUp(self):
        # Do cleanup first so it is ready if an exception is raised
        def kill_patches():  # Create a cleanup callback that undoes our patches
            patch.stopall()  # Stops all patches started with start()
            importlib.reload(app)  # Reload our UUT module which restores the original decorator
            self.calls = Mock()
        self.calls = Mock()
        self.addCleanup(kill_patches)  # We want to make sure this is run so we do this in addCleanup instead of tearDown

        def func(x):
            self.calls()
            return x

        # Now patch the decorator where the decorator is being imported from
        patch('app_decorators.make_pretty', func).start()  # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        # HINT: if you're patching a decor with params use something like:
        # lambda *x, **y: lambda f: f
        importlib.reload(app)  # Reloads the uut.py module which applies our patched decorator

    def test_called(self):
        app.ordinary()
        self.calls.assert_called_once()