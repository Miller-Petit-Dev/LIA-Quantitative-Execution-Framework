# 📘 Guía de Instalación Completa - macOS + VS Code

**LIA Engineering Solutions - Trading Framework**

Esta guía te llevará paso a paso desde cero hasta tener el framework operativo en tu Mac.

---

## 📋 Índice

1. [Requisitos del Sistema](#requisitos-del-sistema)
2. [Instalación de Homebrew](#1-instalación-de-homebrew)
3. [Instalación de Python 3.11](#2-instalación-de-python-311)
4. [Instalación de VS Code](#3-instalación-de-vs-code)
5. [Instalación de MetaTrader 5](#4-instalación-de-metatrader-5)
6. [Configuración del Proyecto](#5-configuración-del-proyecto)
7. [Configuración de VS Code](#6-configuración-de-vs-code)
8. [Primera Ejecución](#7-primera-ejecución)
9. [Verificación del Sistema](#8-verificación-del-sistema)

---

## Requisitos del Sistema

### Hardware

- **Mac**: Intel o Apple Silicon (M1/M2/M3)
- **RAM**: Mínimo 8GB (recomendado 16GB)
- **Disco**: 5GB libres
- **Conexión**: Internet estable

### Software

- **macOS**: Catalina 10.15 o superior
- **Permisos**: Cuenta de administrador

### Conocimientos

- ✅ Uso básico de Terminal
- ✅ Conceptos básicos de Python (deseable)
- ✅ Conocimientos básicos de trading (deseable)

---

## 1. Instalación de Homebrew

Homebrew es el gestor de paquetes para macOS que usaremos para instalar Python.

### 1.1 Abrir Terminal

1. Presiona `Cmd + Espacio`
2. Escribe "Terminal"
3. Presiona `Enter`

### 1.2 Instalar Xcode Command Line Tools

```bash
xcode-select --install
```

- Se abrirá una ventana
- Click en "Instalar"
- Acepta los términos
- Espera a que termine (5-10 minutos)

### 1.3 Instalar Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Importante**: Si usas Apple Silicon (M1/M2/M3), después de instalar ejecuta:

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

### 1.4 Verificar Instalación

```bash
brew --version
```

Deberías ver: `Homebrew X.X.X`

---

## 2. Instalación de Python 3.11

### 2.1 Instalar Python

```bash
brew install python@3.11
```

Espera 5-10 minutos mientras se descarga e instala.

### 2.2 Verificar Instalación

```bash
python3.11 --version
```

Deberías ver: `Python 3.11.X`

### 2.3 Actualizar pip

```bash
python3.11 -m pip install --upgrade pip
```

---

## 3. Instalación de VS Code

### 3.1 Descargar VS Code

1. Ir a [https://code.visualstudio.com/](https://code.visualstudio.com/)
2. Click en "Download Mac Universal"
3. Esperar descarga

### 3.2 Instalar

1. Abrir archivo descargado (.zip)
2. Arrastrar "Visual Studio Code" a carpeta "Aplicaciones"
3. Abrir VS Code desde Aplicaciones

### 3.3 Instalar Extensiones

En VS Code:

1. Click en ícono de extensiones (cuadrados en barra lateral)
2. Buscar e instalar estas extensiones:
   - **Python** (Microsoft)
   - **Pylance** (Microsoft)
   - **Python Indent** (Kevin Rose)

### 3.4 Configurar command line tools

En VS Code, presiona `Cmd + Shift + P` y ejecuta:

```
Shell Command: Install 'code' command in PATH
```

Ahora podrás abrir VS Code desde terminal con `code .`

---

## 4. Instalación de MetaTrader 5

### 4.1 Descargar MT5

1. Ir a [https://www.metatrader5.com/en/download](https://www.metatrader5.com/en/download)
2. Click en "Download MetaTrader 5 for Mac OS"
3. Esperar descarga

### 4.2 Instalar

1. Abrir archivo descargado (.dmg)
2. Arrastrar MetaTrader 5 a Aplicaciones
3. Abrir MetaTrader 5

### 4.3 Abrir Cuenta DEMO

1. En MT5, ir a `File` → `Open an Account`
2. Buscar tu broker (ej: ICMarkets, Pepperstone, XM)
3. Seleccionar "Open a demo account"
4. Completar formulario:
   - **Name**: Tu nombre
   - **Email**: Tu email
   - **Account Type**: Demo
   - **Deposit**: 10,000 USD (o el monto que prefieras)
   - **Leverage**: 1:500
5. Click "Next"
6. **IMPORTANTE**: Guarda estos datos:
   - Login (número de cuenta)
   - Password
   - Server

### 4.4 Verificar Ruta de Instalación

En Terminal:

```bash
ls -la "/Applications/MetaTrader 5.app/Contents/MacOS/MetaTrader 5"
```

Deberías ver el archivo ejecutable. Esta es la ruta que usarás en `.env`.

### 4.5 Habilitar Trading Algorítmico

En MT5:

1. `Tools` → `Options`
2. Pestaña `Expert Advisors`
3. ✅ Marcar **"Allow algo trading"**
4. ✅ Marcar **"Allow DLL imports"**
5. Click `OK`

---

## 5. Configuración del Proyecto

### 5.1 Crear Carpeta de Proyectos

```bash
mkdir -p ~/Documents/Trading
cd ~/Documents/Trading
```

### 5.2 Descargar Proyecto

**Opción A: Con Git**

```bash
git clone <URL_DEL_REPOSITORIO>
cd lia-framework-clean
```

**Opción B: Descargar ZIP**

1. Descargar ZIP del proyecto
2. Extraer en `~/Documents/Trading/`
3. Renombrar carpeta a `lia-framework-clean`

### 5.3 Crear Entorno Virtual

```bash
cd ~/Documents/Trading/lia-framework-clean
python3.11 -m venv venv
```

### 5.4 Activar Entorno Virtual

```bash
source venv/bin/activate
```

Tu terminal debería mostrar `(venv)` al inicio de la línea.

### 5.5 Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Espera 2-3 minutos mientras se instalan las librerías.

### 5.6 Verificar Instalación

```bash
python -c "import MetaTrader5 as mt5; print('MT5 OK:', mt5.__version__)"
python -c "import pandas as pd; print('Pandas OK:', pd.__version__)"
python -c "import pydantic; print('Pydantic OK:', pydantic.__version__)"
```

Deberías ver:
```
MT5 OK: 5.0.45
Pandas OK: 2.0.3
Pydantic OK: 2.5.2
```

### 5.7 Configurar Variables de Entorno

```bash
cp env.example .env
code .env
```

Completar con tus datos de MT5:

```env
MT5_PATH=/Applications/MetaTrader 5.app/Contents/MacOS/MetaTrader 5
MT5_LOGIN=12345678         # Tu número de cuenta DEMO
MT5_PASSWORD=TuPassword    # Tu password DEMO
MT5_SERVER=ICMarkets-Demo  # Tu servidor
MT5_TIMEOUT=60000
MT5_PORTABLE=False
```

**Guardar** (`Cmd + S`) y **cerrar**.

### 5.8 Verificar Conexión con MT5

```bash
python -c "
import MetaTrader5 as mt5
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
result = mt5.initialize(
    path=os.getenv('MT5_PATH'),
    login=int(os.getenv('MT5_LOGIN')),
    password=os.getenv('MT5_PASSWORD'),
    server=os.getenv('MT5_SERVER')
)
if result:
    print('✅ Conexión exitosa con MT5!')
    acc = mt5.account_info()
    print(f'Cuenta: {acc.login}')
    print(f'Balance: {acc.balance} {acc.currency}')
    mt5.shutdown()
else:
    print(f'❌ Error: {mt5.last_error()}')
"
```

Si todo está bien, verás:
```
✅ Conexión exitosa con MT5!
Cuenta: 12345678
Balance: 10000.0 USD
```

---

## 6. Configuración de VS Code

### 6.1 Abrir Proyecto en VS Code

```bash
code ~/Documents/Trading/lia-framework-clean
```

### 6.2 Seleccionar Intérprete de Python

1. Presiona `Cmd + Shift + P`
2. Escribe "Python: Select Interpreter"
3. Selecciona el que dice `./venv/bin/python`

### 6.3 Crear Configuración de Debug

Crear archivo `.vscode/launch.json`:

1. Click en ícono de debug (triángulo con bicho)
2. Click en "create a launch.json file"
3. Seleccionar "Python File"
4. Reemplazar contenido con:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Trading Framework",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal",
            "justMyCode": true,
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    ]
}
```

Guardar (`Cmd + S`).

### 6.4 Crear Configuración de Workspace

Crear archivo `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.formatting.provider": "black",
    "editor.formatOnSave": false,
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/.pytest_cache": true
    },
    "python.analysis.typeCheckingMode": "basic"
}
```

Guardar (`Cmd + S`).

---

## 7. Primera Ejecución

### 7.1 Verificar que MT5 Esté Abierto

1. Abrir MetaTrader 5
2. Verificar que estés conectado (símbolo verde en barra inferior)

### 7.2 Ejecutar Framework

**Opción A: Desde Terminal**

```bash
cd ~/Documents/Trading/lia-framework-clean
source venv/bin/activate
python main.py
```

**Opción B: Desde VS Code**

1. Abrir `main.py`
2. Presionar `F5`

O:

1. Click en ícono de debug
2. Click en botón verde "▶ Trading Framework"

### 7.3 Salida Esperada

```
============================================================
LIA ENGINEERING SOLUTIONS
TRADING FRAMEWORK - EVENT-DRIVEN ARCHITECTURE
============================================================

29/01/2026 14:30:00.123 - Cargando configuración...

✓ Configuración cargada:
  - Símbolos: EURUSD, GBPUSD, USDJPY
  - Timeframe: 1min
  - RSI: Period=14, Upper=70.0, Lower=30.0
  - SL/TP: 50/100 puntos
  - Volumen: 0.01 lotes
  - Max Leverage: 3.0x

29/01/2026 14:30:00.456 - ✓ Cola de eventos inicializada

29/01/2026 14:30:00.789 - Inicializando módulos del framework...

29/01/2026 14:30:01.012 - ✓ Plataforma MT5 inicializada
ℹ Tipo de cuenta: DEMO

------------------------------------------------------------
INFORMACIÓN DE LA CUENTA
------------------------------------------------------------
ID Cuenta:     12345678
Nombre:        Tu Nombre
Broker:        ICMarkets
Servidor:      ICMarkets-Demo
Apalancamiento: 1:500
Divisa:        USD
Balance:       10000.00 USD
Equity:        10000.00 USD
------------------------------------------------------------

... [más inicializaciones] ...

============================================================
SISTEMA LISTO PARA OPERAR
============================================================

29/01/2026 14:30:05.123 - ▶️ Iniciando loop principal...

29/01/2026 14:30:06.456 - 📊 DATA: EURUSD | Close: 1.08456
29/01/2026 14:30:07.789 - 📊 DATA: GBPUSD | Close: 1.27832
29/01/2026 14:30:08.012 - 📊 DATA: USDJPY | Close: 148.234
```

### 7.4 Detener Framework

Presiona `Ctrl + C` en la terminal.

O en VS Code: Click en cuadrado rojo "◼".

---

## 8. Verificación del Sistema

### Checklist de Validación

Ejecuta estos tests para asegurar que todo funciona:

#### ✅ Test 1: Conexión MT5

```bash
python -c "
import MetaTrader5 as mt5
from dotenv import load_dotenv
import os
load_dotenv()
mt5.initialize(path=os.getenv('MT5_PATH'), login=int(os.getenv('MT5_LOGIN')), password=os.getenv('MT5_PASSWORD'), server=os.getenv('MT5_SERVER'))
print('✅ MT5 conectado' if mt5.terminal_info() else '❌ Error MT5')
mt5.shutdown()
"
```

#### ✅ Test 2: Símbolos Disponibles

```bash
python -c "
import MetaTrader5 as mt5
from dotenv import load_dotenv
import os
load_dotenv()
mt5.initialize(path=os.getenv('MT5_PATH'), login=int(os.getenv('MT5_LOGIN')), password=os.getenv('MT5_PASSWORD'), server=os.getenv('MT5_SERVER'))
for symbol in ['EURUSD', 'GBPUSD', 'USDJPY']:
    info = mt5.symbol_info(symbol)
    print(f'{symbol}: ✅' if info else f'{symbol}: ❌ No disponible')
mt5.shutdown()
"
```

#### ✅ Test 3: Obtener Datos

```bash
python -c "
import MetaTrader5 as mt5
from dotenv import load_dotenv
import os
load_dotenv()
mt5.initialize(path=os.getenv('MT5_PATH'), login=int(os.getenv('MT5_LOGIN')), password=os.getenv('MT5_PASSWORD'), server=os.getenv('MT5_SERVER'))
bars = mt5.copy_rates_from_pos('EURUSD', mt5.TIMEFRAME_M1, 0, 10)
print(f'✅ Datos obtenidos: {len(bars)} barras' if bars is not None else '❌ Error al obtener datos')
mt5.shutdown()
"
```

---

## 🎯 Próximos Pasos

Una vez que todo funcione correctamente:

1. ✅ **Dejar correr el framework durante 1 hora** para observar comportamiento
2. ✅ **Revisar logs** para entender cómo funciona
3. ✅ **Ajustar parámetros** en `config/trading_config.py` según necesidad
4. ✅ **Probar en diferentes timeframes** (5min, 15min)
5. ✅ **Monitorear por 1 semana** antes de considerar ajustes mayores

---

## 🐛 Problemas Comunes

### "Command not found: python3.11"

**Solución**:
```bash
brew install python@3.11
brew link python@3.11
```

### "ModuleNotFoundError: No module named 'MetaTrader5'"

**Causa**: Entorno virtual no activado o dependencias no instaladas

**Solución**:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "MT5 error (10004): Invalid parameters"

**Causa**: Credenciales incorrectas en `.env`

**Solución**:
- Verificar `MT5_LOGIN`, `MT5_PASSWORD`, `MT5_SERVER` en `.env`
- Verificar en MT5: Tools → Options → Server

### "Symbol EURUSD not found"

**Causa**: Símbolo no disponible en tu broker

**Solución**:
1. En MT5: View → Market Watch
2. Click derecho → Symbols
3. Buscar símbolos disponibles
4. Actualizar `symbols` en `config/trading_config.py`

---

## ✅ Sistema Instalado Correctamente

Si completaste todos los pasos y los tests pasan, tu sistema está listo.

Puedes proceder a:
- Leer el README principal
- Personalizar la configuración
- Monitorear operaciones

---

## 📞 Soporte

Para problemas técnicos:
1. Revisar esta guía
2. Revisar troubleshooting en README.md
3. Verificar logs en `logs/`

---

**¡Felicitaciones! Tu framework de trading está operativo.**

*LIA Engineering Solutions - Ingeniería que funciona.*
