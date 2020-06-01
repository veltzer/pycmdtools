"""
All configurations for pycmdtools
"""


from pytconf.config import Config, ParamCreator


class ConfigFolder(Config):
    """
    Parameters for the symlink install tool
    """
    folder = ParamCreator.create_existing_folder(
        help_string="Which folder to work on?",
    )


class ConfigUseStandardExceptions(Config):
    """
    Should we use standard exceptions
    """
    use_standard_exceptions = ParamCreator.create_bool(
        help_string="should we use standard exceptions?",
        default=True,
    )


class ConfigChangeLine(Config):
    """
    Change a line in fire parameters
    """
    from_line = ParamCreator.create_str_or_none(
        help_string="from what value?",
        default=None,
    )
    to_line = ParamCreator.create_str(
        help_string="to what value?",
    )
