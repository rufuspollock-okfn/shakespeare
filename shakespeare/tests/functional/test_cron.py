from shakespeare.tests import *

class TestCronController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='cron', action='index'))
        assert 'Cron Jobs' in response
        assert 'work_introductions' in response

    # do not test as requires external access
    def _test_work_introductions(self):
        response = self.app.get(url(controller='cron', action='work_introductions'))
        assert '[' in response

