// Получаем объект Telegram Web App
const tg = window.Telegram.WebApp;

// Инициализация приложения
tg.expand(); // Развернуть приложение на весь экран

// Находим кнопку и текстовый элемент
const button = document.getElementById('mainButton');
const result = document.getElementById('result');

// Обработчик нажатия на кнопку
button.addEventListener('click', () => {
  result.textContent = 'Кнопка нажата!';
  tg.MainButton.setText('Отправить').show();
});

// Обработчик нажатия на MainButton
tg.MainButton.onClick(() => {
  alert('MainButton нажата!');
});