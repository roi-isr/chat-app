import os

import motor.motor_asyncio

mongo_client = os.getenv('MONGO_URL')
client = motor.motor_asyncio.AsyncIOMotorClient(mongo_client)
db_connection = client.app
