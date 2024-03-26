from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

class Gpsdata(Model):
    latitude=fields.FloatField()
    longitude=fields.FloatField()
    speed=fields.FloatField()
    heading=fields.FloatField()

Gpsdata_pydantic=pydantic_model_creator(Gpsdata,name="Gpsdata")
Gpsdata_pydanticIn=pydantic_model_creator(Gpsdata,name="Gpsdata",exclude_readonly=True)
