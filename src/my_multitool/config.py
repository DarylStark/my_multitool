"""Module with the API for configuration.

This module contains the class to retrive and save configuration for the CLI
application.
"""

import re
from os.path import expanduser

import yaml
from pydantic import BaseModel, Extra, ValidationError

from .exceptions import (ConfigFileNotFoundException,
                         ConfigFileNotValidException, NoConfigToSaveException)


class ContextModel(BaseModel):
    """BaseModel for contexts.

    Contains the fields for a context.

    Attributes:
        name: the name of the context.
        db_string: the database connection string for the context.
        warning: determines if a warning should be given
    """

    name: str
    db_string: str
    warning: bool = False
    service_user: str | None = None
    service_pass: str | None = None
    root_user: str | None = None

    class Config:
        """Configuration for the model.

        We disallow extra fields. This makes sure the user cannot specify
        fields that are not defined. This results in a more robust
        configuration.
        """

        extra = Extra.forbid

    @property
    def db_string_with_masked_pwd(self) -> str:
        """Property for the database string with a maked password.

        This property returns the db string with the password masked. The
        password will be displayed as three asteriks. This can be useful
        for displaying the db string on screen without revealing sensitive
        information.

        Returns:
            The DB string without the password.
        """
        return re.sub(r'//(\S+):(\S+)@',
                      lambda x: f'//{x.group(1)}:***@',
                      self.db_string)


class ConfigModel(BaseModel):
    """Base settings for the complete config.

    Contains the fields for a complete config. Normally, these are retrieved
    from a YAML file.

    Attributes:
        active_context: the currently activated context.
        contexts: a list with configured contexts.
    """

    active_context: str
    contexts: list[ContextModel] = []

    class Config:
        """Configuration for the model.

        We disallow extra fields. This makes sure the user cannot specify
        fields that are not defined. This results in a more robust
        configuration.
        """

        extra = Extra.forbid


class ConfigManager:
    """Manager for the configfile.

    Manages the configfile. Retrieves and save the settings made in a
    YAML configfile.
    """

    def __init__(self) -> None:
        """Initiate default values.

        Sets the default values for the internal variables.
        """
        self.yaml_file: str = ''
        self.config: ConfigModel = ConfigModel(active_context='default')

    def configure(self, yaml_file: str) -> None:
        """Configure the config-object.

        Set the configurationvalues for the config object.

        Args:
            yaml_file: the filename for the YAML file.
        """
        self.yaml_file = expanduser(yaml_file)

    def load(self) -> None:
        """Load the configuration from the file.

        Loads the configuration and applies the model to it. If the file is
        correct, the configuration gets saved in the object and can be used by
        the application.

        Raises:
            ConfigFileNotFoundException: when the given configfile is not
                found or not entered.
            ConfigFileNotValidException: when the given configfile is not
                correct.
        """
        if not self.yaml_file:
            raise ConfigFileNotFoundException

        try:
            with open(self.yaml_file, 'r', encoding='utf-8') as input_file:
                content = yaml.safe_load(input_file)
        except FileNotFoundError as exc:
            raise ConfigFileNotFoundException from exc

        # Create a ConfigModel of it
        try:
            self.config = ConfigModel(**content)
        except ValidationError as exc:
            raise ConfigFileNotValidException from exc

    def save(self) -> None:
        """Save the configuration to file.

        Saves the configuration to the specified file.

        Raises:
            NoConfigToSaveException: when the config is not set yet.
        """
        if self.config and self.yaml_file:
            with open(self.yaml_file, 'w', encoding='utf-8') as output_file:
                yaml.dump(self.config.dict(), output_file)
        else:
            raise NoConfigToSaveException('Configuration not set yet')

    def set_default_config(self) -> None:
        """Set default config.

        Method to set the default config for the object. This can be used as a
        default for when there is no config.
        """
        self.config = ConfigModel(active_context='default', contexts=[
            ContextModel(name='default', db_string='sqlite:///:memory:')
        ])

    @property
    def contexts(self) -> dict[str, ContextModel]:
        """Get the configured contexts.

        Returns the configured context as a dict where the key the name of the
        context is.

        Returns:
            A dictionary where the key the name of the context is, and the
            value the ContextModel instance for the context or, if the config
            is not set; None.
        """
        if getattr(self, 'config', None) is None:
            self.load()

        return {
            context.name: context for context in self.config.contexts
        }

    @property
    def full_config(self) -> ConfigModel:
        """Get the full configuration.

        Returns the full configuration.

        Returns:
            The ConfigModel.
        """
        if getattr(self, 'config', None) is None:
            self.load()
        return self.config

    @property
    def active_context(self) -> ContextModel:
        """Get the active Context.

        Returns the active context.

        Returns:
            The ContextModel for the active context.
        """
        if getattr(self, 'config', None) is None:
            self.load()
        return self.contexts[self.config.active_context]
