from blueprints.admin import bp as admin_bp
from blueprints.hotmovie_douban import bp as hotmovie_bp
from blueprints.watchlist_service import bp as watchlist_bp
from blueprints.setting import bp as setting_bp
from blueprints.register import bp as register_bp

#BLUEPRINTS模块化
def register_blueprints(app):
    app.register_blueprint(admin_bp)
    app.register_blueprint(setting_bp)
    app.register_blueprint(hotmovie_bp)
    app.register_blueprint(watchlist_bp)
    app.register_blueprint(register_bp)