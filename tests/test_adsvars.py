import unittest2
from src.adsclientthread_package_tchobtrong.utils.ads_vars import Ads_Var


class Ads_Var_Testcase(unittest2.TestCase):
    '''
    Test cases for ADS Var
    '''

    def test_abletocreate_bool_data(self):

        adsvar = Ads_Var(adsname='Test.bTest',datatype='BOOL')

        isBool = isinstance(adsvar.value, bool)

        self.assertEqual(isBool, True, 'The value shall be boolen.')
        self.assertEqual(adsvar.value, False, 'The default shall be False.')



