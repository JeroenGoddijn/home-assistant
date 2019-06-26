from homeassistant import config_entries

@config_entries.HANDLERS.register(DOMAIN)
class ExampleConfigFlow(config_entries.ConfigFlow):

    async def async_step_user(self, info):
        if info is not None:
            # process info

        return self.async_show_form(
            step_id='init',
            data_schema=vol.Schema({
              vol.Required('password'): str
            })
        )    