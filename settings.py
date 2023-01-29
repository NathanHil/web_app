import mimetypes
mimetypes.add_type("text/css", ".css", True)

TESTING = 'test' in sys.argv[1:]

INSTALLED_APPS = (
    'test_without_migrations'
)

if TESTING:
    print('=========================')
    print('In TEST Mode - Disableling Migrations')
    print('=========================')

    class DisableMigrations(object):

        def __contains__(self, item):
            return True

        def __getitem__(self, item):
            return "notmigrations"

    MIGRATION_MODULES = DisableMigrations()