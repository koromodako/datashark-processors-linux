"""Datashark Linux Plugin
"""
from ds_core.api import Artifact, Result, Status
from ds_core.meta import PluginMeta
from ds_core.config import DSConfiguration
from ds_core.plugin import Plugin, generic_plugin_test_app
from ds_core.database import Format
from . import NAME, LOGGER


class LinuxPlugin(Plugin, metaclass=PluginMeta):
    """Process files extracted from a Linux host"""

    NAME = NAME
    DEPENDS_ON = []
    DESCRIPTION = """
    Refine data from Linux host files
    """
    YARA_RULE_BODY = Plugin.YARA_MATCH_ALL

    def process(self, artifact: Artifact) -> Result:
        """Process a VHD disk image"""
        try:
            # TODO: perform artifact processing here
            # commit data added by plugin
            self.session.commit()
            # finally set overall processing status to SUCCESS
            status = Status.SUCCESS
        except:
            LOGGER.exception(
                "an exception occured while processing artifact: %s", artifact
            )
            status = Status.FAILURE
        return Result(self, status, artifact)


def instanciate(config: DSConfiguration):
    """Instanciate plugin"""
    return LinuxPlugin(config)


def test():
    """Test plugin"""
    generic_plugin_test_app(instanciate, Format.DATA)
