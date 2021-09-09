"""Datashark psort.py Processor
"""
from typing import List
from asyncio.subprocess import PIPE, DEVNULL
from datashark_core.meta import ProcessorMeta
from datashark_core.logging import LOGGING_MANAGER
from datashark_core.processor import ProcessorInterface, ProcessorError
from datashark_core.model.api import Kind, System, ProcessorArgument

NAME = 'linux_psort'
LOGGER = LOGGING_MANAGER.get_logger(NAME)


class PSortProcessor(ProcessorInterface, metaclass=ProcessorMeta):
    """Wraps psort.py"""

    NAME = NAME
    SYSTEM = System.LINUX
    ARGUMENTS = []
    DESCRIPTION = """
    Run psort with given arguments
    """

    async def _run(self, arguments: List[ProcessorArgument]):
        """Process a file using psort.py"""
