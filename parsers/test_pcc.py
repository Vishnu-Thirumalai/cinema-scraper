import unittest
from pcc import PCC

from datetime import datetime
from datetime import time
from datetime import date



class TestPCC(unittest.TestCase):

    def test_get_url(self):
        sd = date(1988,7,16)
        ed = date(3000,1,1)
        url = PCC.getURL(sd,ed)

        expected_url = "https://princecharlescinema.com/PrinceCharlesCinema.dll/WhatsOn?sd=16&sm=7&sy=1988&ed=2&em=1&ey=3000"
        self.assertEqual(url[86],"2","Date not correctly incremented")
        self.assertEqual(url, expected_url, "Incorrect URL returned")

    def test_dateParse(self):
        dt = PCC.parseDate("Sun 19 Mar 2023", "6:30pm")
        today = datetime(2023,3,19,18,30)
        self.assertEqual(dt, today, "Didn't parse Sun 19 Mar 2023 6:30pm correctly")

    def test_dateParse_today(self):
        dt = PCC.parseDate("Today", "12:00am")
        today = datetime.combine( date.today(),time(0,0,0) )
        self.assertEqual(dt, today, "Didn't parse \"Today\" correctly")




if __name__ == '__main__':
    unittest.main()