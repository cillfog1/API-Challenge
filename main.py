from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from haversine import haversine

app = FastAPI()

#---------------------- Sample Database ----------------------
# test lat: 53.3252185, test long: -6.2550504
shop_far = {
    'latitude': 51.533848,
    'longitude': -0.318844,
    'merchantId': 0,
    'merchantName': 'Tesco Metro (London)'
}

shop_close = {
    'latitude': 53.321165,
    'longitude': -6.266164,
    'merchantId': 1,
    'merchantName': 'Tesco Metro (Rathmines)'
}

shop_between = {
    'latitude': 53.348072,
    'longitude': -6.265225,
    'merchantId': 2,
    'merchantName': 'Tesco Metro (Quays)'
}


#---------------------- Initialise Database ----------------------
db = [shop_far, shop_close, shop_between]
ids = [9]

#---------------------- Dictionary Parameters (BaseModel) ----------------------
class Merchant(BaseModel):
    latitude: float
    longitude: float
    merchantId: int
    merchantName: str

class MerchantIn(BaseModel):
    latitude: float
    longitude: float
    merchantName: str

class MerchantUpdate(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    merchantName: Optional[str] = None


@app.get("/")
async def index():
    return "Creating API using FastAPI"


#---------------------- Create Merchant ----------------------
# creating merchant and storing in database
# returns new merchant created
@app.post('/merchants', response_model=Merchant)
async def create_merchant(merchant: MerchantIn):
    merchant_dict = merchant.dict()
    if not ids:
        id = len(db)
    else:
        id = ids[0]
        ids.pop(0)
    merchant_dict.update({'merchantId': id})
    db.insert(id, merchant_dict)
    return merchant_dict


#---------------------- Update Merchant ----------------------
# updates merchant with only given variables sent
# returns new updated merchant
@app.patch('/merchants/{merchantId}', response_model=Merchant)
async def update_merchant(merchantId: int, merchant: MerchantUpdate):
    stored_merchant = Merchant(**await find_merchant(merchantId))
    update_data = merchant.dict(exclude_unset=True)
    updated_merchant = stored_merchant.copy(update=update_data)
    db[await find_merchant_index(merchantId)] = updated_merchant.dict()
    return updated_merchant


#---------------------- Get Merchants In Order Of Proximity (Haversine) ----------------------
# gets all merchants and calculates haversine for each
# returns merchantNames in order of proximity using haversine
@app.get('/merchants')
async def get_merchants(lat: float, long: float):
    distances = await find_haversine(lat, long)
    return [i[1].get('merchantName') for i in distances]


#---------------------- Get Merchant By ID ----------------------
# returns merchant associated with passed in merchantId
@app.get('/merchants/{merchantId}', response_model=Merchant)
async def get_merchant(merchantId: int):
    return await find_merchant(merchantId)


#---------------------- Delete Merchant ----------------------
# deletes merchant associated with passed in merchantId
# deletes the merchant from database and returns the deleted merchant
@app.delete('/merchants/{merchantId}', response_model=Merchant)
async def delete_merchant(merchantId: int):
    merchant = await find_merchant(merchantId)
    db.remove(merchant)
    ids.append(merchantId)
    return merchant

#---------------------- Helper Functions ----------------------
# returns merchant with a given id
async def find_merchant(id):
    for merchant in db:
        if merchant.get('merchantId') == id:
            return merchant


# returns index location of merchant in database associated with passed in id
async def find_merchant_index(id):
    for index, merchant in enumerate(db):
        if merchant.get('merchantId') == id:
            return index


#---------------------- Get Haversine For Each Merchant ----------------------
# calculates haversine distance for all merchants in database given latitude and longitude arguments
# creates tuple with distance of merchant and merchant dict
# returns a sorted list of tuples in order of proximity
async def find_haversine(lat, long):
    merchant_distances = []
    for merchant in db:
        distance = haversine((lat, long), (merchant.get('latitude'), merchant.get('longitude')))
        merchant_distances.append((distance, merchant))
    return sorted(merchant_distances, key=lambda x: x[0])


# test for haversine
if __name__ == '__main__':
    print(find_haversine(53.3252185, -6.2550504))


#--ToRun: python -m uvicorn main:app --reload