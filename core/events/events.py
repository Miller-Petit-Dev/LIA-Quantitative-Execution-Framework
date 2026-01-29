"""
LIA Engineering Solutions - Trading Framework
Sistema de Eventos - Arquitectura Event-Driven

Este módulo define todos los eventos que fluyen por el framework.
Cada evento representa un estado o acción específica en el ciclo de trading.
"""

from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
import pandas as pd
from typing import Optional


class EventType(str, Enum):
    """Tipos de eventos soportados por el framework"""
    DATA = "DATA"
    SIGNAL = "SIGNAL"
    SIZING = "SIZING"
    ORDER = "ORDER"
    EXECUTION = "EXECUTION"
    PENDING = "PENDING"


class SignalType(str, Enum):
    """Tipos de señales de trading"""
    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, Enum):
    """Tipos de órdenes de trading"""
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"


# ============================================================================
# BASE EVENT
# ============================================================================

class BaseEvent(BaseModel):
    """
    Evento base del cual heredan todos los demás eventos.
    Garantiza que todos los eventos tengan un tipo identificable.
    """
    event_type: EventType
    
    class Config:
        arbitrary_types_allowed = True


# ============================================================================
# DATA EVENT
# ============================================================================

class DataEvent(BaseEvent):
    """
    Evento generado cuando hay nuevos datos de mercado disponibles.
    
    Atributos:
        symbol: Símbolo del instrumento financiero
        data: Serie de pandas con OHLCV y otros datos de la barra
    """
    event_type: EventType = EventType.DATA
    symbol: str
    data: pd.Series


# ============================================================================
# SIGNAL EVENT
# ============================================================================

class SignalEvent(BaseEvent):
    """
    Evento generado por el generador de señales cuando se identifica
    una oportunidad de trading.
    
    Atributos:
        symbol: Símbolo del instrumento
        signal: Tipo de señal (BUY/SELL)
        target_order: Tipo de orden a ejecutar
        target_price: Precio objetivo (para órdenes pending)
        magic_number: Identificador único de la estrategia
        sl: Stop Loss
        tp: Take Profit
    """
    event_type: EventType = EventType.SIGNAL
    symbol: str
    signal: SignalType
    target_order: OrderType
    target_price: float
    magic_number: int
    sl: float = 0.0
    tp: float = 0.0


# ============================================================================
# SIZING EVENT
# ============================================================================

class SizingEvent(BaseEvent):
    """
    Evento generado después de calcular el tamaño de la posición.
    Incluye todos los datos del SignalEvent más el volumen calculado.
    
    Atributos:
        volume: Tamaño de la posición en lotes
    """
    event_type: EventType = EventType.SIZING
    symbol: str
    signal: SignalType
    target_order: OrderType
    target_price: float
    magic_number: int
    sl: float = 0.0
    tp: float = 0.0
    volume: float


# ============================================================================
# ORDER EVENT
# ============================================================================

class OrderEvent(BaseEvent):
    """
    Evento generado después de pasar por el risk manager.
    Representa una orden lista para ser ejecutada.
    
    El volumen puede haber sido ajustado por el risk manager.
    """
    event_type: EventType = EventType.ORDER
    symbol: str
    signal: SignalType
    target_order: OrderType
    target_price: float
    magic_number: int
    sl: float = 0.0
    tp: float = 0.0
    volume: float


# ============================================================================
# EXECUTION EVENT
# ============================================================================

class ExecutionEvent(BaseEvent):
    """
    Evento generado cuando una orden ha sido ejecutada exitosamente.
    
    Atributos:
        fill_price: Precio al que se ejecutó la orden
        fill_time: Timestamp de ejecución
    """
    event_type: EventType = EventType.EXECUTION
    symbol: str
    signal: SignalType
    fill_price: float
    fill_time: datetime
    volume: float


# ============================================================================
# PENDING ORDER EVENT
# ============================================================================

class PlacedPendingOrderEvent(BaseEvent):
    """
    Evento generado cuando una orden pending ha sido colocada exitosamente.
    """
    event_type: EventType = EventType.PENDING
    symbol: str
    signal: SignalType
    target_order: OrderType
    target_price: float
    magic_number: int
    sl: float = 0.0
    tp: float = 0.0
    volume: float
