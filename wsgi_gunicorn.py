from factory import create_app, celery_app

app = create_app(config_name="DEVELOPMENT")
app.app_context().push()
