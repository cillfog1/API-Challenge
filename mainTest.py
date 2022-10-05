import unittest
import asyncio
import main

class MainTest(unittest.TestCase):

#---------------------- Get Merchants In Order Of Proximity (Haversine) ----------------------
    def testGetMerchants(self):
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(main.get_merchants(53.3252185, -6.2550504))
        expectedResult = ['Tesco Metro (Rathmines)', 'Tesco Metro (Quays)', 'Tesco Metro (London)']
        self.assertEqual(result, expectedResult)


#---------------------- Get Merchant By ID ----------------------
    def testGetMerchantByID(self):
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(main.get_merchant(1))
        expectedResult = {
               'latitude': 53.321165,
               'longitude': -6.266164,
               'merchantId': 1,
               'merchantName': 'Tesco Metro (Rathmines)'
        }
        self.assertEqual(result, expectedResult)
   

#---------------------- Helper Functions ----------------------
    def testFindMerchantByID(self):
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(main.find_merchant(1))
        expectedResult = {
               'latitude': 53.321165,
               'longitude': -6.266164,
               'merchantId': 1,
               'merchantName': 'Tesco Metro (Rathmines)'
        }
        self.assertEqual(result, expectedResult)


    def testFindMerchantIndex(self):
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(main.find_merchant_index(1))
        expectedResult = 1
        self.assertEqual(result, expectedResult)


#---------------------- Get Haversine For Each Merchant ----------------------
    def testFindHarersine(self):
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(main.find_haversine(53.3252185, -6.2550504))
        expectedResult = [
            (0.8648663263364303, {'latitude': 53.321165, 'longitude': -6.266164, 'merchantId': 1, 'merchantName': 'Tesco Metro (Rathmines)'}),
            (2.6294584367407317, {'latitude': 53.348072, 'longitude': -6.265225, 'merchantId': 2, 'merchantName': 'Tesco Metro (Quays)'}),
            (448.8772650742687, {'latitude': 51.533848, 'longitude': -0.318844, 'merchantId': 0, 'merchantName': 'Tesco Metro (London)'})
        ]
        self.assertEqual(result, expectedResult)


if __name__ == '__main__':
    unittest.main()