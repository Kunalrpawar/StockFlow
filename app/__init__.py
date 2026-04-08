from flask import Flask
from flask.cli import with_appcontext
import click

from app.extensions import db, migrate
from app.routes.alert_routes import alert_bp
from app.routes.product_routes import product_bp
from config.settings import Config


def create_app(config_object: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(product_bp)
    app.register_blueprint(alert_bp)

    @app.get("/health")
    def health_check():
        return {"status": "ok"}, 200

    @app.cli.command("seed-data")
    @with_appcontext
    def seed_data_command():
        from app.seed import seed_sample_data

        seed_sample_data()
        click.echo("Sample seed data inserted")

    from app.models import (  # noqa: F401
        company,
        inventory,
        inventory_log,
        product,
        product_bundle,
        product_supplier,
        sales_record,
        supplier,
        warehouse,
    )

    return app
