![Banner](./LIABanner.png)

# 🚀 LIA Quantitative Execution - Trading Framework

**Framework Profesional de Trading Algorítmico Event-Driven para MetaTrader 5**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MT5](https://img.shields.io/badge/MetaTrader-5-green.svg)](https://www.metatrader5.com/)
[![License](https://img.shields.io/badge/license-Proprietary-red.svg)]()

---

## 📖 Descripción

Este framework implementa una **arquitectura event-driven** (basada en eventos) para trading algorítmico profesional. Desarrollado por **LIA Engineering Solutions**, combina principios sólidos de ingeniería de software con estrategias cuantitativas de trading.

### ¿Qué hace?

✅ Monitorea mercados en tiempo real  
✅ Genera señales basadas en indicadores técnicos (RSI)  
✅ Calcula tamaños de posición apropiados  
✅ Valida riesgo antes de ejecutar  
✅ Ejecuta órdenes automáticamente en MT5  
✅ Notifica sobre operaciones realizadas  

### Principios de Diseño

🎯 **Separación de responsabilidades**: Cada módulo tiene una función específica  
🔄 **Event-driven**: Comunicación asíncrona entre componentes  
🔧 **Extensible**: Fácil agregar nuevas estrategias  
📚 **Mantenible**: Código limpio y documentado  
🏭 **Production-ready**: Preparado para operar en real (con precaución)  

---

## 🏗 Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                  TRADING DIRECTOR                            │
│                (Orquestador Central)                         │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  Events Queue   │
                  └─────────────────┘
                           │
      ┌────────────────────┼────────────────────┐
      │                    │                    │
      ▼                    ▼                    ▼
┌──────────┐         ┌──────────┐        ┌──────────┐
│   Data   │────────▶│  Signal  │───────▶│ Position │
│ Provider │         │Generator │        │  Sizer   │
└──────────┘         └──────────┘        └──────────┘
                                                │
                                                ▼
                                         ┌──────────┐
                                         │   Risk   │
                                         │ Manager  │
                                         └──────────┘
                                                │
                                                ▼
                                         ┌──────────┐
                                         │  Order   │
                                         │ Executor │
                                         └──────────┘
```

---

## ✨ Características

### Core

- ✅ Arquitectura Event-Driven completa
- ✅ Estrategia RSI (Mean Reversion)
- ✅ Risk Management por leverage factor
- ✅ Position Sizing (volumen fijo)
- ✅ Multi-símbolo simultáneo
- ✅ Stop Loss / Take Profit automáticos
- ✅ Notificaciones (Consola + Telegram opcional)

### Seguridad

- 🔐 Variables de entorno para credenciales
- ⚠️ Advertencia en cuentas reales
- 🛡️ Validación de leverage
- 📊 Logging detallado

---

## 📦 Instalación Rápida

### Requisitos

- macOS 10.15+
- Python 3.11+
- MetaTrader 5
- Cuenta DEMO en un broker

### Pasos

```bash
# 1. Clonar proyecto
git clone <REPO_URL>
cd lia-framework-clean

# 2. Crear entorno virtual
python3.11 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar .env
cp env.example .env
# Editar .env con tus credenciales

# 5. Ejecutar
python main.py
```

---

## ⚙️ Configuración

### Variables de Entorno (.env)

```env
MT5_PATH=/Applications/MetaTrader 5.app/Contents/MacOS/MetaTrader 5
MT5_LOGIN=12345678
MT5_PASSWORD=TuPassword
MT5_SERVER=ICMarkets-Demo
MT5_TIMEOUT=60000
MT5_PORTABLE=False
```

### Parámetros de Estrategia (config/trading_config.py)

```python
TradingConfig(
    symbols=['EURUSD', 'GBPUSD', 'USDJPY'],
    timeframe='1min',
    
    # RSI
    rsi_period=14,
    rsi_upper=70.0,
    rsi_lower=30.0,
    sl_points=50,
    tp_points=100,
    
    # Sizing
    fixed_volume=0.01,
    
    # Risk
    max_leverage_factor=3.0
)
```

---

## 🚀 Uso

### Ejecutar el Framework

```bash
# Activar entorno
source venv/bin/activate

# Ejecutar
python main.py
```

### Salida Esperada

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

...

============================================================
SISTEMA LISTO PARA OPERAR
============================================================

29/01/2026 14:30:05.789 - 📊 DATA: EURUSD | Close: 1.08456
```

### Detener

Presiona `Ctrl + C`

---

## 📁 Estructura del Proyecto

```
lia-framework-clean/
├── config/
│   └── trading_config.py          # Configuración centralizada
├── core/
│   ├── events/
│   │   └── events.py               # Sistema de eventos
│   └── utils/
│       └── utils.py                # Utilidades comunes
├── modules/
│   ├── platform_connector/
│   ├── data_provider/
│   ├── signal_generator/
│   ├── position_sizer/
│   ├── risk_manager/
│   ├── order_executor/
│   ├── portfolio/
│   ├── notifications/
│   └── trading_director/
├── logs/                           # Logs (se crea automáticamente)
├── .env                            # Credenciales (NO SUBIR A GIT)
├── .env.example                    # Template
├── requirements.txt
├── main.py                         # Punto de entrada
└── README.md
```

---

## 🎨 Personalización

### Cambiar Símbolos

```python
# config/trading_config.py
symbols=['XAUUSD', 'BTCUSD']  # Oro y Bitcoin
```

### Ajustar RSI

```python
rsi_period=21,       # Más suave
rsi_upper=75.0,      # Menos señales
rsi_lower=25.0
```

### Mayor Volumen

```python
fixed_volume=0.05,          # 5 micro lotes
max_leverage_factor=5.0      # Mayor exposición
```

---

## 🐛 Troubleshooting

### Error: "No se puede conectar a MT5"

✅ Verificar que MT5 esté abierto  
✅ Revisar credenciales en `.env`  
✅ Confirmar servidor online  

### Error: "Symbol not found"

✅ Verificar símbolos disponibles en tu broker  
✅ Actualizar `symbols` en `config/trading_config.py`  

### No genera señales

✅ Operar en horario de mercado activo  
✅ Ajustar niveles RSI (ej: 65/35 en lugar de 70/30)  
✅ Verificar que no hay posiciones abiertas  

---

## ✅ Mejores Prácticas

### Desarrollo

1. **Siempre usa cuenta DEMO**
2. **Comienza con volúmenes pequeños** (0.01 lotes)
3. **Monitorea logs continuamente**
4. **Backtesting primero**
5. **Paper trading mínimo 30 días**

### Producción

1. **Cuenta REAL solo cuando estés seguro**
2. **Leverage conservador** (max 3x)
3. **Diversifica símbolos**
4. **Monitoreo diario**
5. **Backups de configuración**

### Seguridad

1. **Nunca subas `.env` a Git**
2. **Contraseñas seguras**
3. **2FA en broker**
4. **No compartas credenciales**

---

## 📚 Documentación Completa

Para guía detallada de instalación paso a paso en macOS + VS Code, ver:

📘 **[INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)**

---

## 📞 Soporte

### Problemas

1. Revisa Troubleshooting
2. Verifica logs en `logs/`
3. Consulta documentación MT5

### Contribuciones

Bienvenidas siguiendo:
- Código limpio y documentado
- Respeto a arquitectura event-driven
- Tests para nuevas features

---

## ⚠️ AVISO DE RIESGO

**El trading de instrumentos financieros conlleva riesgos significativos.**

Este software se proporciona "tal cual" sin garantías de ningún tipo.  
El usuario asume toda la responsabilidad por el uso del sistema.

- ❌ No garantizamos ganancias
- ❌ No somos asesores financieros
- ✅ Usa SOLO capital que puedas permitirte perder

---

## 📄 Licencia

Copyright © 2026 **LIA Engineering Solutions**

Todos los derechos reservados.

Permitido para uso educativo y de investigación.

---

## 🎯 Roadmap

- [x] Arquitectura event-driven
- [x] Estrategia RSI
- [x] Risk Management
- [ ] Backtesting engine
- [ ] Dashboard web
- [ ] Múltiples estrategias
- [ ] Machine Learning integration

---

**Desarrollado con criterio de ingeniería, pensado para operar.**

*LIA Engineering Solutions - Acelerando decisiones, diseño y ejecución.*

---

## 🔗 Navegación

<p align="center">
  <a href="https://github.com/miller-petit-dev/Nexus-AI-Financial-Data-Pipeline-Insights">
    <img src="https://img.shields.io/badge/Ir_a_Nexus-NEXUS_AI-0078D4?style=for-the-badge&logo=databricks&logoColor=white" alt="Ir a Nexus">
  </a>
  &nbsp;&nbsp;
  <a href="https://github.com/Miller-Petit-Dev/aurum-edge">
    <img src="https://img.shields.io/badge/Ir_a_Aurum-AURUM_EDGE-D4AF37?style=for-the-badge&logo=bitcoin&logoColor=black" alt="Ir a Aurum">
  </a>
  &nbsp;&nbsp;
  <a href="https://github.com/Miller-Petit-Dev">
    <img src="https://img.shields.io/badge/Volver_al_Home-Portfolio-333333?style=for-the-badge&logo=github&logoColor=white" alt="Volver al Home">
  </a>
</p>
