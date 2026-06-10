@echo off
:: Script para subir cambios a GitHub automáticamente

echo Iniciando proceso de subida a GitHub...
git add .
echo.
set /p mensaje="Por favor, escribe el mensaje del commit: "
git commit -m "%mensaje%"
git push
echo.
echo ¡Listo, Fran! Cambios subidos correctamente al servidor.
pause