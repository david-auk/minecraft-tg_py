# Import handlers here so their loaded by the entrypoint
import app.telegram.handlers.auth
import app.telegram.handlers.common # Load common last due to Catch-all handlers