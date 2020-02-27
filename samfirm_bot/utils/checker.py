""" check given arguments """
from samfirm_bot.samfirm_bot import SAM_FIRM


async def is_device(model):
    """ check if the given model is a correct one"""
    return bool(model in SAM_FIRM.models)


async def is_region(region):
    """ check if the given region is a correct one"""
    return bool(region in SAM_FIRM.regions)
