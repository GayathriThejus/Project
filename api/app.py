from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from models import Gpsdata,Gpsdata_pydantic,Gpsdata_pydanticIn


app=FastAPI()

@app.get('/')
def index():
    return {'Msg':"read from docs"}


@app.post('/gpsdata')
async def add_gpsdata(gpsinfo:Gpsdata_pydanticIn):
    gpdsdata_obj= await Gpsdata.create(**gpsinfo.dict(exclude_unset = True))
    response = await Gpsdata_pydantic.from_tortoise_orm(gpdsdata_obj)
    return {'status' :'ok', 'data': response}

@app.get('/gpsdata')
async def get_gpsdata():
    response=await Gpsdata_pydantic.from_queryset(Gpsdata.all())
    return {"status":"ok","data":response}

register_tortoise(
    app,
    db_url="sqlite://database.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)