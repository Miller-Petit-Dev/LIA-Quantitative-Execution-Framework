"""
LIA Engineering Solutions - Trading Framework
Position Sizer - Calculador de Tamaño de Posición

Implementa método de sizing por volumen fijo.
Puede extenderse para soportar risk-based sizing.
"""

from core.events.events import SignalEvent, SizingEvent
from core.utils.utils import Utils
from queue import Queue
import MetaTrader5 as mt5


class PositionSizer:
    """
    Calcula el tamaño de posición para cada señal.
    """
    
    def __init__(self, events_queue: Queue, fixed_volume: float = 0.01):
        """
        Inicializa el position sizer.
        
        Args:
            events_queue: Cola de eventos del sistema
            fixed_volume: Volumen fijo a operar (en lotes)
        """
        self.events_queue = events_queue
        self.fixed_volume = fixed_volume
        
        print(
            f"{Utils.dateprint()} - ✓ Position Sizer inicializado: "
            f"Volumen fijo = {fixed_volume} lotes"
        )
    
    
    def size_signal(self, signal_event: SignalEvent) -> None:
        """
        Calcula el tamaño de la posición y genera SizingEvent.
        
        Args:
            signal_event: Señal de trading a procesar
        """
        symbol = signal_event.symbol
        
        # Validar volumen mínimo del símbolo
        symbol_info = mt5.symbol_info(symbol)
        
        if symbol_info is None:
            print(
                f"{Utils.dateprint()} - ERROR: No se pudo obtener info de {symbol}"
            )
            return
        
        volume_min = symbol_info.volume_min
        volume_step = symbol_info.volume_step
        
        # Ajustar volumen al step permitido
        volume = max(self.fixed_volume, volume_min)
        volume = round(volume / volume_step) * volume_step
        
        # Validar volumen final
        if volume < volume_min:
            print(
                f"{Utils.dateprint()} - ERROR: Volumen {volume} menor al mínimo "
                f"{volume_min} para {symbol}"
            )
            return
        
        # Crear SizingEvent
        sizing_event = SizingEvent(
            symbol=signal_event.symbol,
            signal=signal_event.signal,
            target_order=signal_event.target_order,
            target_price=signal_event.target_price,
            magic_number=signal_event.magic_number,
            sl=signal_event.sl,
            tp=signal_event.tp,
            volume=volume
        )
        
        # Encolar evento
        self.events_queue.put(sizing_event)
        
        print(
            f"{Utils.dateprint()} - 📐 SIZING: {signal_event.signal} {symbol} "
            f"| Volumen calculado: {volume} lotes"
        )
