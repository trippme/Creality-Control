import logging
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_PASSWORD
import voluptuous as vol

_LOGGER = logging.getLogger(__name__)

class CrealityControlConfigFlow(config_entries.ConfigFlow, domain="creality_control"):
    """Handle a config flow for Creality Control."""
    
    def __init__(self):
        _LOGGER.debug("Initializing config flow for Creality Control.")
        self._host = None
        self._port = None
        self._password = None

    async def async_step_user(self, user_input=None):
        _LOGGER.debug("Entering async_step_user.")

        if user_input is not None:
            self._host = user_input.get(CONF_HOST)
            self._port = user_input.get(CONF_PORT)
            self._password = user_input.get(CONF_PASSWORD)
            _LOGGER.debug(f"User input received: Host={self._host}, Port={self._port}, Password={self._password}")

            # Validate the host and port
            if not self._host or not self._port:
                _LOGGER.error("Host and Port are required")
                return self.async_abort(reason="missing_required_fields")

            # Successfully received user input, create the entry
            return self.async_create_entry(
                title="Creality Control",
                data={CONF_HOST: self._host, CONF_PORT: self._port, CONF_PASSWORD: self._password or ""},
            )
        
        # If no user input, show the form
        return self.async_show_form(
            step_id="user", 
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_PORT, default=18188): int,
                vol.Optional(CONF_PASSWORD, default=""): str  # Make the password optional
            })
        )

    async def async_step_import(self, import_config):
        """Handle import of configuration via YAML."""
        _LOGGER.debug("Import step triggered with config: %s", import_config)
        return await self.async_step_user(import_config)
