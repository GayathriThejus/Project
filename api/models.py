from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

class Gpsdata(Model):
    latitude=fields.FloatField()
    longitude=fields.FloatField()
    speed=fields.FloatField()
    heading=fields.FloatField()

class User(Model):
    username=fields.TextField()
    userid=fields.IntField(pk=True)
    password=fields.TextField()

# class Bus(Model):
#     bus_id=fields.IntField(pk=True)
#     user=fields.ForeignKeyField('models.User',related_name="buses")

# class BusDetails(Model):
#     bus=fields.IntField(pk=True)
#     starting_pt=fields.JSONField()
#     ending_pt=fields.JSONField()
#     stops=fields.JSONField()
#     userid=fields.ForeignKeyField('models.User',related_name="buses")
    
class BusDetailsEve(Model):
    bus=fields.IntField(pk=True)
    school_pt=fields.JSONField()
    end_pt=fields.JSONField()
    stops=fields.JSONField()
    


Gpsdata_pydantic=pydantic_model_creator(Gpsdata,name="Gpsdata")
Gpsdata_pydanticIn=pydantic_model_creator(Gpsdata,name="Gpsdata",exclude_readonly=True)
user_model=pydantic_model_creator(User,name="UserLogin")
user_modelIn=pydantic_model_creator(User,name="UserLoginIn",exclude_readonly=True)
# busreg_model=pydantic_model_creator(Bus,name="Bus")
# busreg_modelIn=pydantic_model_creator(Bus,name="BusIn",exclude_readonly=True)
# bus_model=pydantic_model_creator(BusDetails,name="BusDetails")
# bus_modelIn=pydantic_model_creator(BusDetails,name="BusDetailsIn",exclude_readonly=True)
bus_model=pydantic_model_creator(BusDetailsEve,name='BusDetailsEve')
bus_modelIn=pydantic_model_creator(BusDetailsEve,name='BusDetailsEve',exclude_readonly=True)