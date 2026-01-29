"""
LIA Engineering Solutions - Trading Framework
Signal Generator - Generador de Señales de Trading

Implementa estrategia RSI (Relative Strength Index) para mean reversion.

Lógica:
- RSI < 30 (sobreventa) → Señal BUY
- RSI > 70 (sobrecompra) → Señal SELL
- Una posición abierta por símbolo a la vez
"""

from core.events.events import DataEvent, SignalEvent, SignalType, OrderType
from core.utils.utils import Utils
from modules.data_provider.data_provider import DataProvider
from modules.portfolio.portfolio import Portfolio
from modules.order_executor.order_executor import OrderExecutor
from queue import Queue
from typing import Optional
import pandas as pd


class SignalGenerator:
    """
    Genera señales de trading basadas en RSI.
    """
    
    def __init__(
        self,
        events_queue: Queue,
        data_provider: DataProvider,
        portfolio: Portfolio,
        order_executor: OrderExecutor,
        magic_number: int,
        timeframe: str = "1min",
        rsi_period: int = 14,
        rsi_upper: float = 70.0,
        rsi_lower: float = 30.0,
        sl_points: int = 50,
        tp_points: int = 100
    ):
        """
        Inicializa el generador de señales RSI.
        
        Args:
            events_queue: Cola de eventos del sistema
            data_provider: Proveedor de datos de mercado
            portfolio: Gestor de portfolio
            order_executor: Ejecutor de órdenes
            magic_number: Identificador de la estrategia
            timeframe: Timeframe a operar
            rsi_period: Período del RSI
            rsi_upper: Nivel de sobrecompra
            rsi_lower: Nivel de sobreventa
            sl_points: Stop Loss en puntos
            tp_points: Take Profit en puntos
        """
        self.events_queue = events_queue
        self.DATA_PROVIDER = data_provider
        self.PORTFOLIO = portfolio
        self.ORDER_EXECUTOR = order_executor
        self.magic_number = magic_number
        
        # Parámetros de la estrategia
        self.timeframe = timeframe
        self.rsi_period = rsi_period
        self.rsi_upper = rsi_upper
        self.rsi_lower = rsi_lower
        self.sl_points = sl_points
        self.tp_points = tp_points
        
        print(
            f"{Utils.dateprint()} - ✓ Signal Generator (RSI) inicializado: "
            f"RSI Period={rsi_period}, Upper={rsi_upper}, Lower={rsi_lower}"
        )
    
    
    def _calculate_rsi(self, prices: pd.Series, period: int) -> float:
        """
        Calcula el RSI (Relative Strength Index).
        
        Args:
            prices: Serie de precios de cierre
            period: Período del RSI
            
        Returns:
            Valor del RSI (0-100)
        """
        if len(prices) < period + 1:
            return 50.0  # Valor neutro si no hay suficientes datos
        
        # Calcular cambios
        delta = prices.diff()
        
        # Separar ganancias y pérdidas
        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)
        
        # Promedios móviles
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()
        
        # Evitar división por cero
        if avg_loss.iloc[-1] == 0:
            return 100.0
        
        # Calcular RSI
        rs = avg_gain.iloc[-1] / avg_loss.iloc[-1]
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    
    def generate_signal(self, data_event: DataEvent) -> None:
        """
        Genera señal de trading basada en RSI.
        
        Reglas:
        1. Obtener histórico de precios
        2. Calcular RSI
        3. Evaluar condiciones de entrada
        4. Verificar que no haya posición abierta
        5. Generar SignalEvent si corresponde
        
        Args:
            data_event: Evento con nuevos datos de mercado
        """
        symbol = data_event.symbol
        
        # 1. Obtener datos históricos
        bars = self.DATA_PROVIDER.get_latest_closed_bars(
            symbol=symbol,
            timeframe=self.timeframe,
            num_bars=self.rsi_period + 10  # Buffer adicional
        )
        
        if bars.empty or len(bars) < self.rsi_period + 1:
            return  # No hay suficientes datos
        
        # 2. Calcular RSI
        rsi = self._calculate_rsi(bars['close'], self.rsi_period)
        
        # 3. Verificar que no haya posición abierta
        open_positions = self.PORTFOLIO.get_number_of_strategy_open_positions_by_symbol(symbol)
        
        if open_positions["TOTAL"] > 0:
            return  # Ya hay posición abierta
        
        # 4. Evaluar condiciones de entrada
        signal_type: Optional[SignalType] = None
        
        if rsi < self.rsi_lower:
            # Sobreventa → BUY
            signal_type = SignalType.BUY
            
        elif rsi > self.rsi_upper:
            # Sobrecompra → SELL
            signal_type = SignalType.SELL
        
        # 5. Generar señal si corresponde
        if signal_type is not None:
            # Obtener precio actual
            tick = self.DATA_PROVIDER.get_latest_tick(symbol)
            current_price = tick.get('bid', data_event.data['close'])
            
            # Calcular SL y TP
            point = 0.0001 if 'JPY' not in symbol else 0.01
            
            if signal_type == SignalType.BUY:
                sl = current_price - (self.sl_points * point)
                tp = current_price + (self.tp_points * point)
            else:  # SELL
                sl = current_price + (self.sl_points * point)
                tp = current_price - (self.tp_points * point)
            
            # Crear evento de señal
            signal_event = SignalEvent(
                symbol=symbol,
                signal=signal_type,
                target_order=OrderType.MARKET,
                target_price=current_price,
                magic_number=self.magic_number,
                sl=sl,
                tp=tp
            )
            
            # Encolar señal
            self.events_queue.put(signal_event)
            
            print(
                f"{Utils.dateprint()} - 📊 SEÑAL GENERADA: {signal_type} {symbol} "
                f"| RSI={rsi:.2f} | SL={sl:.5f} | TP={tp:.5f}"
            )
