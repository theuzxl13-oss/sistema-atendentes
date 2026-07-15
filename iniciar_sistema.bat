@echo off
title Iniciando Sistema Futturis...
echo Iniciando o Servidor do Aplicativo...
start "" cmd /c "py -m streamlit run novo_app.py"
echo Servidor iniciado com sucesso! O navegador abrira automaticamente.
timeout /t 5
exit