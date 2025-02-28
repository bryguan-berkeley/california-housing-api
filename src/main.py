
import logging 
import os
from contextlib import asynccontextmanager
from joblib import load
from fastapi import FastAPI
from fastapi_cache import FastAPICache
import redis.asyncio as aioredis
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

####################################################################################################

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan_mechanism(app: FastAPI):
    logger.info('API Starting')

    global model
    model = load('model.pkl')
    
    redis_url = os.getenv('redis_url', 'redis://localhost:6379')
    redis = aioredis.from_url(redis_url)
    FastAPICache.init(RedisBackend(redis), prefix = 'api-cache')
    
    yield

    logger.info('API Ending')

api = FastAPI(lifespan = lifespan_mechanism)

####################################################################################################

from src.pydantic import Pydantic_Single_Input, Pydantic_Single_Output, Pydantic_Multiple_Inputs, Pydantic_Multiple_Outputs

@api.post('/single-predict', response_model = Pydantic_Single_Output)
@cache(expire = 60)
async def single_predict(house: Pydantic_Single_Input):
    prediction = model.predict(house.vectorize())
    return Pydantic_Single_Output(prediction = prediction)

@api.post('/multiple-predict', response_model = Pydantic_Multiple_Outputs)
@cache(expire = 60)
async def multiple_predict(houses: Pydantic_Multiple_Inputs):
    predictions = model.predict(houses.vectorize())
    return Pydantic_Multiple_Outputs(predictions = predictions)

####################################################################################################

@api.get('/health')
async def health():
    return {'Status': 'Healthy'}