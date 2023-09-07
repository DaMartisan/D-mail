from flask import Flask, render_template, request, redirect, url_for
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import smtplib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\Work\D-mail/database.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class GreetingCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    abonent_number = db.Column(db.String(50))
    full_name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    usage_period = db.Column(db.String(100))
    previous_data = db.Column(db.String(100))
    current_data = db.Column(db.String(100))
    greeting_text = db.Column(db.Text)

# Создание таблицы в базе данных
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('show_bd'))

@app.route('/send_sms', methods=['POST'])
def send_sms():
    # Получение данных открытки из POST-запроса
    abonent_number = request.form['abonent_number']
    full_name = request.form['full_name']
    address = request.form['address']
    usage_period = request.form['usage_period']
    previous_data = request.form['previous_data']
    current_data = request.form['current_data']
    greeting_text = request.form.get('greeting_text', '')  # Дополнительное поле: текст поздравления (необязательно)

    # Создание текста сообщения с данными открытки
    message = f'Абонентский номер: {abonent_number}\n'
    message += f'ФИО абонента: {full_name}\n'
    message += f'Адрес: {address}\n'
    message += f'Период использования услугой: {usage_period}\n'
    message += f'Данные за предыдущий период: {previous_data}\n'
    message += f'Данные за текущий период: {current_data}\n'
    message += f'Текст поздравления: {greeting_text}\n'

    # Отправка сообщения по электронной почте через Gmail
    sender_email = 'buskindaniil0@gmail.com'
    sender_password = 'pwidygskeqbxkkzo'
    recipient_email = 'buracenkovika29@gmail.com'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = 'Отправка открытки по электросети'
    msg.attach(MIMEText(message, 'plain'))

    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login(sender_email, sender_password)
    smtp_server.send_message(msg)
    smtp_server.quit()

    # Создание записи в базе данных
    greeting_card = GreetingCard(
        abonent_number=abonent_number,
        full_name=full_name,
        address=address,
        usage_period=usage_period,
        previous_data=previous_data,
        current_data=current_data,
        greeting_text=greeting_text
    )
    db.session.add(greeting_card)
    db.session.commit()

    # Перенаправление на страницу greeting_cards.html
    return redirect(url_for('show_greeting_cards'))

@app.route('/bd', methods=['GET'])
def show_bd():
    greeting_cards = GreetingCard.query.all()
    return render_template('BD.html', cards=greeting_cards)

@app.route('/greeting_cards', methods=['GET'])
def show_greeting_cards():
    greeting_cards = GreetingCard.query.all()
    return render_template('greeting_cards.html', cards=greeting_cards)

if __name__ == '__main__':
    app.run()
