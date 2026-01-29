# 🚀 Guía de Referencia Rápida

**LIA Engineering Solutions - Trading Framework**

Comandos y configuraciones esenciales para uso diario.

---

## ⚡ Comandos Rápidos

### Activar Entorno y Ejecutar

```bash
cd ~/Documents/Trading/lia-framework-clean
source venv/bin/activate
python main.py
```

### Detener Framework

```
Ctrl + C
```

### Ver Logs en Tiempo Real

```bash
tail -f logs/*.log
```

### Limpiar Cache de Python

```bash
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

---

## 📝 Configuración Rápida

### Cambiar Símbolos

Editar `config/trading_config.py`:

```python
symbols=['XAUUSD', 'BTCUSD']  # Oro y Bitcoin
```

### Cambiar Timeframe

```python
timeframe='5min'  # 1min, 5min, 15min, 1h, 4h, 1d
```

### Ajustar RSI

```python
rsi_period=21,      # Más suave (default: 14)
rsi_upper=75.0,     # Menos señales SELL (default: 70.0)
rsi_lower=25.0      # Menos señales BUY (default: 30.0)
```

### Ajustar SL/TP

```python
sl_points=100,      # Stop Loss más amplio (default: 50)
tp_points=200       # Take Profit mayor (default: 100)
```

### Cambiar Volumen

```python
fixed_volume=0.05   # 5 micro lotes (default: 0.01)
```

### Ajustar Risk Management

```python
max_leverage_factor=5.0  # Mayor exposición (default: 3.0)
```

---

## 🔧 Verificaciones Rápidas

### Verificar Conexión MT5

```bash
python -c "
import MetaTrader5 as mt5
from dotenv import load_dotenv
import os
load_dotenv()
mt5.initialize(path=os.getenv('MT5_PATH'), login=int(os.getenv('MT5_LOGIN')), password=os.getenv('MT5_PASSWORD'), server=os.getenv('MT5_SERVER'))
print('✅ Conectado' if mt5.terminal_info() else '❌ Error')
mt5.shutdown()
"
```

### Ver Símbolos Disponibles

```bash
python -c "
import MetaTrader5 as mt5
from dotenv import load_dotenv
import os
load_dotenv()
mt5.initialize(path=os.getenv('MT5_PATH'), login=int(os.getenv('MT5_LOGIN')), password=os.getenv('MT5_PASSWORD'), server=os.getenv('MT5_SERVER'))
symbols = mt5.symbols_get()
for s in symbols[:20]:
    print(s.name)
mt5.shutdown()
"
```

### Verificar Balance

```bash
python -c "
import MetaTrader5 as mt5
from dotenv import load_dotenv
import os
load_dotenv()
mt5.initialize(path=os.getenv('MT5_PATH'), login=int(os.getenv('MT5_LOGIN')), password=os.getenv('MT5_PASSWORD'), server=os.getenv('MT5_SERVER'))
acc = mt5.account_info()
print(f'Balance: {acc.balance} {acc.currency}')
print(f'Equity: {acc.equity} {acc.currency}')
mt5.shutdown()
"
```

---

## 🎨 Personalización Común

### Estrategia Más Agresiva

```python
# config/trading_config.py
TradingConfig(
    symbols=['EURUSD', 'GBPUSD', 'XAUUSD'],
    timeframe='1min',
    
    # RSI más sensible
    rsi_period=10,
    rsi_upper=65.0,
    rsi_lower=35.0,
    
    # SL/TP más ajustados
    sl_points=30,
    tp_points=60,
    
    # Mayor volumen
    fixed_volume=0.05,
    
    # Mayor leverage
    max_leverage_factor=5.0
)
```

### Estrategia Más Conservadora

```python
# config/trading_config.py
TradingConfig(
    symbols=['EURUSD'],
    timeframe='15min',
    
    # RSI más estricto
    rsi_period=21,
    rsi_upper=75.0,
    rsi_lower=25.0,
    
    # SL/TP más amplios
    sl_points=100,
    tp_points=300,
    
    # Menor volumen
    fixed_volume=0.01,
    
    # Menor leverage
    max_leverage_factor=2.0
)
```

### Swing Trading (Largo Plazo)

```python
# config/trading_config.py
TradingConfig(
    symbols=['EURUSD', 'GBPUSD'],
    timeframe='4h',           # 4 horas
    
    rsi_period=14,
    rsi_upper=70.0,
    rsi_lower=30.0,
    
    sl_points=200,
    tp_points=500,
    
    fixed_volume=0.02,
    max_leverage_factor=2.0
)
```

---

## 📊 Monitoreo

### Archivos a Revisar Diariamente

1. **Consola/Terminal**: Salida en tiempo real
2. **logs/*.log**: Historial detallado
3. **MT5**: Posiciones y balance
4. **config/trading_config.py**: Parámetros activos

### Métricas Clave

- **Señales generadas**: Cuántas señales por día
- **Órdenes ejecutadas**: Cuántas se convirtieron en trades
- **Órdenes rechazadas**: Por risk manager
- **Win rate**: % de trades ganadores
- **P&L**: Ganancia/pérdida acumulada

---

## ⚠️ Checklist Pre-Trading

Antes de dejar correr el framework:

- [ ] MT5 está abierto y conectado
- [ ] Cuenta es DEMO (para pruebas)
- [ ] Variables en `.env` son correctas
- [ ] `config/trading_config.py` revisado
- [ ] Símbolos están disponibles en broker
- [ ] Trading algorítmico habilitado en MT5
- [ ] Entorno virtual activado
- [ ] Suficiente balance en cuenta

---

## 🐛 Troubleshooting Rápido

| Problema | Solución |
|----------|----------|
| No genera señales | Ajustar niveles RSI (65/35) |
| Error MT5 | Verificar que MT5 esté abierto |
| Symbol not found | Revisar símbolos en broker |
| Órdenes rechazadas | Reducir `fixed_volume` o aumentar `max_leverage_factor` |
| Framework se detiene | Revisar logs para error específico |

---

## 🔐 Seguridad Rápida

### Cambiar a Cuenta Real (CON PRECAUCIÓN)

1. **Abrir cuenta REAL en broker**
2. **Actualizar `.env`**:
   ```env
   MT5_LOGIN=98765432        # Número de cuenta REAL
   MT5_PASSWORD=NuevoPass
   MT5_SERVER=Broker-Real
   ```
3. **Reducir configuración**:
   ```python
   fixed_volume=0.01         # Mínimo volumen
   max_leverage_factor=2.0   # Conservador
   ```
4. **Monitoreo continuo las primeras 24h**

---

## 📚 Recursos Útiles

### Documentación

- [MetaTrader 5 Python](https://www.mql5.com/en/docs/python_metatrader5)
- [Pandas](https://pandas.pydata.org/docs/)
- [Pydantic](https://docs.pydantic.dev/)

### Trading

- [Babypips](https://www.babypips.com/)
- [Investopedia](https://www.investopedia.com/)

---

## 💡 Tips de Uso

1. **Comenzar siempre en DEMO**
2. **Monitorear al menos 1 semana** antes de ajustar
3. **Un cambio a la vez** (no cambiar todo junto)
4. **Mantener logs** de cambios y resultados
5. **Backups regulares** de configuración

---

## 🎯 Workflow Diario Recomendado

### Mañana (Inicio de Sesión)

```bash
# 1. Activar entorno
cd ~/Documents/Trading/lia-framework-clean
source venv/bin/activate

# 2. Verificar MT5 está abierto
open -a "MetaTrader 5"

# 3. Ejecutar framework
python main.py
```

### Durante el Día

- Monitorear consola cada 1-2 horas
- Revisar posiciones en MT5
- Anotar señales generadas

### Noche (Fin de Sesión)

```bash
# 1. Detener framework
Ctrl + C

# 2. Revisar logs del día
cat logs/*.log | grep "SIGNAL\|EXECUTION"

# 3. Cerrar MT5 si no hay posiciones abiertas
```

---

**¡Listo para operar con criterio de ingeniería!**

*LIA Engineering Solutions*
