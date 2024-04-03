from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from models import Gpsdata,Gpsdata_pydantic,Gpsdata_pydanticIn,user_model,bus_model,User,BusDetailsEve,bus_modelIn
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()



origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers = ['*']
)


@app.get('/')
def index():
    return {'Msg':"read from docs"}


@app.post('/gpsdata')
async def add_gpsdata(gpsinfo:Gpsdata_pydantic):
    gpdsdata_obj= await Gpsdata.create(**gpsinfo.dict(exclude_unset = True))
    response = await Gpsdata_pydantic.from_tortoise_orm(gpdsdata_obj)
    return {'status' :'ok', 'data': response}

@app.get('/gpsdata')
async def get_gpsdata():
    response=await Gpsdata_pydantic.from_queryset(Gpsdata.all())
    return {"status":"ok","data":response}

@app.get('/getbusdetailseve')
async def getbusdet():
    response=await bus_model.from_queryset(BusDetailsEve.all())
    return {"status":"ok","data":response}

@app.post('/busdet_eve')
async def busdetails(businfo:bus_model):
    bus_obj=await BusDetailsEve.create(**businfo.dict(exclude_unset=True))
    response=await bus_model.from_tortoise_orm(bus_obj)
    return {"status":"ok","data":response}

@app.put('/busdet_eve/{bus_id}')
async def update_busdata(bus_id : int, update_info: bus_modelIn):
    bus = await BusDetailsEve.get(bus= bus_id)
    update_info = update_info.dict(exclude_unset = True)
    bus.school_pt=update_info['school_pt']
    bus.end_pt=update_info['end_pt']
    bus.stops=update_info['stops']
    await bus.save()
    response= await bus_model.from_tortoise_orm(bus)
    return {'status':'ok','data':response}

@app.get('/userdata')
async def get_userdata():
    response=await user_model.from_queryset(User.all())
    return {"status":"ok","data":response}


@app.post('/userdata')
async def add_userdata(userinfo:user_model):
    user_obj=await User.create(**userinfo.dict(exclude_unset=True))
    response=await user_model.from_tortoise_orm(user_obj)
    return {"status":"ok","data":response}

@app.get('/busregdata')
async def get_busregdata():
    response=await bus_model.from_queryset(BusDetails.all().values('bus', 'userid'))
    return {"status":"ok","data":response}


@app.post('/busregdata/{user_id}')
async def add_busregdata(user_id:int,busreginfo:bus_model):
    user_det=await User.get(userid=user_id)
    bus_obj=await Bus.create(**busreginfo.dict(),user=user_det)
    response=await bus_model.from_tortoise_orm(bus_obj)
    return {"status":"ok","data":response}


@app.get('/busdata')
async def get_busdata():
    response=await bus_model.from_queryset(BusDetails.all())
    return {"status":"ok","data":response}

@app.post('/busdata/{bus_id}')
async def add_busdata(bus_id:int,businfo:bus_model):
    bus_det=await Bus.get(bus_id=bus_id)
    bus_obj=await BusDetails.create(**businfo.dict(),bus=bus_det)
    response=await bus_model.from_tortoise_orm(bus_obj)
    return {"status":"ok","data":response}

@app.get('/mapdata/{user_id}')
async def mapdata(user_id:int):
    user_det=await User.get(userid=user_id)
    print(user_det)
    bus_det=await Bus.get(user=user_det)
    bus_details=await BusDetails.get(bus=bus_det)
    return {"data":bus_details}
    


register_tortoise(
    app,
    db_url="sqlite://database.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)