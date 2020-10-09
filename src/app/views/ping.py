import logging


logger = logging.getLogger(__name__)


async def can_we_enjoy() -> str:
    logger.info("We know how to give pleasure here and now ^_^")

    return "Account service is working :) Enjoy with us ^_^"
