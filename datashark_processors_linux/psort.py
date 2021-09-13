"""Datashark psort.py Processor
"""
from typing import Dict
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
    ARGUMENTS = [
        {
            'name': 'analysis',
            'kind': Kind.STR,
            'required': False,
            'description': """
                A comma separated list of analysis plugin names to be loaded
            """,
        },
        {
            'name': 'slice',
            'kind': Kind.STR,
            'required': False,
            'description': """
                Date and time to create a time slice around. This parameter, if defined, will display all events that
                happened X minutes before and after the defined date, where X is controlled by the --slice_size option,
                which is 5 minutes by default. The date and time must be specified in ISO 8601 format including time
                zone offset, for example: 20200619T20:09:23+02:00
            """,
        },
        {
            'name': 'slicer',
            'kind': Kind.STR,
            'required': False,
            'description': """
                Create a time slice around every filter match. This parameter, if defined will save all X events before
                and after a filter match has been made. X is defined by the --slice_size parameter
            """,
        },
        {
            'name': 'slice_size',
            'kind': Kind.INT,
            'required': False,
            'description': """
                Defines the slice size. In the case of a regular time slice it defines the number of minutes the slice
                size should be. In the case of the --slicer it determines the number of events before and after a filter
                match has been made that will be included in the result set. The default value is 5.
                See --slice or --slicer for more details about this option
            """,
        },
        {
            'name': 'output_format',
            'kind': Kind.STR,
            'value': 'l2tcsv',
            'required': False,
            'description': "The output format",
        },
        {
            'name': 'output_file',
            'kind': Kind.PATH,
            'required': True,
            'description': "Output filename",
        },
        {
            'name': 'storage_file',
            'kind': Kind.PATH,
            'required': True,
            'description': "Path to a storage file",
        },
        {
            'name': 'filter',
            'kind': Kind.STR,
            'required': False,
            'description': """
                A filter that can be used to filter the dataset before it is written into storage. More information
                about the filters and how to use them can be found here:
                https://plaso.readthedocs.io/en/latest/sources/user/Event-filters.html
            """,
        },
    ]
    DESCRIPTION = """
    Run psort with given arguments
    """

    async def _run(self, arguments: Dict[str, ProcessorArgument]):
        """Process a file using psort.py"""
        proc = await self._start_subprocess(
            'datashark.processors.psort.bin',
            ['-q', '-u'],
            [
                # optional
                ('analysis', '--analysis'),
                ('slice', '--slice'),
                ('slicer', '--slicer'),
                ('slice_size', '--slice-size'),
                ('output_format', '--output-format'),
                ('output_file', '--write'),
                # positional
                ('storage_file', None),
                ('filter', None),
            ],
            arguments,
            stdout=DEVNULL,
            stderr=PIPE,
        )
        await self._handle_communicating_process(proc)
