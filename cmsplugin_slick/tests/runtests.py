import django
import os, sys
gettext = lambda s: s

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../'))
sys.path.append(BASE_DIR)
os.chdir(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cmsplugin_slick.tests.settings")

django.setup()
from django.test.runner import DiscoverRunner
test_runner = DiscoverRunner(verbosity=2)

failures = test_runner.run_tests(['cmsplugin_slick'])
if failures:
    sys.exit(failures)