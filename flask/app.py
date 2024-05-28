from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

# Создание экземпляра приложения Flask
app = Flask(__name__)
# Создание экземпляра API для управления ресурсами
api = Api(app)
# Конфигурация базы данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///equipment.db'
# Создание экземпляра SQLAlchemy для работы с базой данных
db = SQLAlchemy(app)

# Определение модели данных для изображения оборудования
class EquipmentImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор изображения
    image_url = db.Column(db.String(255), nullable=False)  # URL изображения

    def __repr__(self):
        return f'<EquipmentImage {self.id}>'  # Представление объекта в удобочитаемом формате

# Класс для загрузки изображений
class ImageUpload(Resource):
    def post(self):
        try:
            image_data = request.get_json()  # Получение данных из запроса
            new_image = EquipmentImage(image_url=image_data['image_url'])  # Создание нового объекта изображения
            db.session.add(new_image)  # Добавление объекта в сессию базы данных
            db.session.commit()  # Сохранение изменений в базе данных
            return jsonify(new_image.id), 200  # Возврат ID нового изображения
        except Exception as e:
            return jsonify(error=str(e)), 500  # Возврат ошибки, если операция не удалась

# Класс для получения изображений по ID
class ImageGet(Resource):
    def get(self, image_id):
        try:
            image = EquipmentImage.query.get(image_id)  # Поиск изображения по ID
            if image:
                return jsonify(image_url=image.image_url), 200  # Возврат URL изображения, если найдено
            else:
                return jsonify(error="Image not found"), 404  # Сообщение об ошибке, если изображение не найдено
        except Exception as e:
            return jsonify(error=str(e)), 500  # Возврат ошибки, если запрос не удался

# Регистрация ресурсов API
api.add_resource(ImageUpload, '/upload')
api.add_resource(ImageGet, '/images/<int:image_id>')

# Маршрут по умолчанию для проверки работоспособности сервиса
@app.route('/')
def home():
    return jsonify({'message': 'Добро пожаловать в службу сбора изображений оборудования'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создание таблиц в базе данных
    app.run(debug=True)  # Запуск приложения в режиме отладки