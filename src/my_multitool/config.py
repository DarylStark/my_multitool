"""Module with the API for configuration.

This module contains the class to retrive and save configuration for the CLI
application.
"""

from pydantic import BaseModel, Extra, ValidationError
import yaml
from .exceptions import (ConfigFileNotFoundException,
                         ConfigFileNotValidException)


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

    class Config:
        """Configuration for the model.

        We disallow extra fields. This makes sure the user cannot specify
        fields that are not defined. This results in a more robust
        configuration.
        """
        extra = Extra.forbid


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

    def __init__(self, yaml_file: str, create: bool = True) -> None:
        """Initiator saves the default values.

        Args:
            yaml_file: the filename for the YAML file.
            create: determines if the file has to be created if it does not
                exist.
        """
        self.yaml_file = yaml_file
        self.config: ConfigModel | None = None

    def load(self) -> None:
        """Load the configuration from the file.

        Loads the configuration and applies the model to it. If the file is
        correct, the configuration gets saved in the object and can be used by
        the application.
        """
        try:
            with open(self.yaml_file, 'r') as input_file:
                content = yaml.safe_load(input_file)
        except FileNotFoundError:
            raise ConfigFileNotFoundException

        # Create a ConfigModel of it
        try:
            self.config = ConfigModel(**content)
        except ValidationError:
            raise ConfigFileNotValidException

    def save(self) -> None:
        """Save the configuration to file.

        Saves the configuration to the specified file.
        """
        raise NotImplementedError

    @property
    def contexts(self) -> dict[str, ContextModel] | None:
        """Get the configured contexts.

        Returns the configured context as a dict where the key the name of the
        context is.

        Returns:
            A dictionary where the key the name of the context is, and the
            value the ContextModel instance for the context or, if the config
            is not set; None.
        """
        if self.config:
            return {
                context.name: context for context in self.config.contexts
            }
        return None
