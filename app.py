import dash

app = dash.Dash()
server = app.server
app.config.suppress_callback_exceptions = True
app.scripts.config.serve_locally=True
app.css.config.serve_locally=True