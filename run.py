from app import create_app
from app.routes.questionnaire_routes import questionnaire_bp

app = create_app()
app.register_blueprint(questionnaire_bp, url_prefix='/questionnaire')

if __name__ == '__main__':
    app.run(debug=True)
