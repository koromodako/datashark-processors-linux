"""Datashark Binwalk Processor
"""
from typing import Dict
from asyncio.subprocess import PIPE, DEVNULL
from datashark_core.meta import ProcessorMeta
from datashark_core.logging import LOGGING_MANAGER
from datashark_core.processor import ProcessorInterface
from datashark_core.model.api import Kind, System, ProcessorArgument

NAME = 'linux_binwalk'
LOGGER = LOGGING_MANAGER.get_logger(NAME)


class BinwalkProcessor(ProcessorInterface, metaclass=ProcessorMeta):
    """Run binwalk on given filepath"""

    NAME = NAME
    SYSTEM = System.LINUX
    ARGUMENTS = [
        {
            'name': 'extract',
            'kind': Kind.BOOL,
            'value': 'false',
            'required': False,
            'description': "Automatically extract known file types",
        },
        {
            'name': 'directory',
            'kind': Kind.PATH,
            'required': False,
            'description': "Directory to store extracted files",
        },
        {
            'name': 'size_limit',
            'kind': Kind.INT,
            'required': False,
            'description': "Limit the size of each extracted file",
        },
        {
            'name': 'count_limit',
            'kind': Kind.INT,
            'required': False,
            'description': "Limit the number of extracted files",
        },
        {
            'name': 'length',
            'kind': Kind.INT,
            'required': False,
            'description': "Number of bytes to scan",
        },
        {
            'name': 'offset',
            'kind': Kind.INT,
            'required': False,
            'description': "Start scan at this file offset",
        },
        {
            'name': 'base',
            'kind': Kind.INT,
            'required': False,
            'description': "Add a base address to all printed offsets",
        },
        {
            'name': 'block',
            'kind': Kind.INT,
            'required': False,
            'description': "Set file block size",
        },
        {
            'name': 'swap',
            'kind': Kind.INT,
            'required': False,
            'description': "Reverse every n bytes before scanning",
        },
        {
            'name': 'csv',
            'kind': Kind.BOOL,
            'value': 'false',
            'required': False,
            'description': "Log results to file in CSV format",
        },
        {
            'name': 'log',
            'kind': Kind.PATH,
            'required': True,
            'description': "Log results to file",
        },
        {
            'name': 'filepath',
            'kind': Kind.PATH,
            'required': True,
            'description': "File to process",
        },
    ]
    DESCRIPTION = """
    Run binwalk on given filepath
    """

    async def _run(self, arguments: Dict[str, ProcessorArgument]):
        """Process a file using binwalk"""
        # invoke subprocess
        proc = await self._start_subprocess(
            'datashark.processors.binwalk.bin',
            ['-q'],
            [
                # optional
                ('extract', '-e'),
                ('directory', '-C'),
                ('size_limit', '-j'),
                ('count_limit', '-n'),
                ('length', '-l'),
                ('offset', '-o'),
                ('base', '-O'),
                ('block', '-K'),
                ('swap', '-g'),
                ('csv', '-c'),
                ('log', '-f'),
                # positional
                ('filepath', None),
            ],
            arguments,
            stdout=DEVNULL,
            stderr=PIPE,
        )
        await self._handle_communicating_process(proc)
