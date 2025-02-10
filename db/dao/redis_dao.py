import aioredis

REDIS_HOST_IP = "192.168.3.39"
REDIS_PORT = 6379


async def get_redis():
    return await aioredis.from_url(f"redis://{REDIS_HOST_IP}:{REDIS_PORT}", decode_responses=True)
