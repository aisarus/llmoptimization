# Vegan Recipe Builder · Desktop (Electron)

Однофайловый UI + локальная БД (IndexedDB) в десктоп-приложении.

## Запуск
1) Установи Node.js 18+
2) В папке проекта:
   ```bash
   npm install
   npm run dev   # или npm start
   ```

## Сборка установщика
- Windows: `npm run build:win`  → NSIS .exe в `dist/`
- macOS:   `npm run build:mac`  → .dmg в `dist/`
- Linux:   `npm run build:linux`→ .AppImage в `dist/`

## Импорт пресетов
Админ → «Пакеты пресетов» → выбери `assets/demo_pack.json`.

## Данные
Все данные хранятся локально в IndexedDB браузерного движка Electron.
