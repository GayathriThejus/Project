from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from models import Gpsdata,Gpsdata_pydantic,Gpsdata_pydanticIn,user_model,bus_model,User,BusDetailsEve,bus_modelIn
from fastapi.middleware.cors import CORSMiddleware
from geopy.distance import distance

app=FastAPI()

origins=['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

@app.get('/getbusdetailseve/{bus_id}')
async def getbusdet(bus_id:int):
    response=await bus_model.from_queryset_single(BusDetailsEve.get(bus =bus_id))
    distances=[]
    i=0
    for stop in response.stops:
        if i == 0:
            lat = response.school_pt['latitude']
            long = response.school_pt['longitude']
            stop=response.stops[0]
            lat2=stop['pt']['latitude']
            long2=stop['pt']['longitude']
            i+=1
        else:
            stop=response.stops[i-1]
            lat = stop['pt']['latitude']
            long=stop['pt']['longitude']
            stop2=response.stops[i]
            lat2 = stop2['pt']['latitude']
            long2=stop2['pt']['longitude']
            i+=1

        location=float(lat),float(long)
        location2=float(lat2),float(long2)
        dist=distance(location,location2).kilometers
        distances.append(dist)
    avg_speed=40
    time=[]
    for dist in distances:
        t=dist/avg_speed
        t_min=t*60
        time.append(t_min)

    return {"status":"ok","data":{"distances":distances,"time":time,"other_data":response}}
    

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

@app.get('/busregdata/{bus_id}')
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