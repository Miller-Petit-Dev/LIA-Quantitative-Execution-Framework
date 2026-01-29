"""
LIA Engineering Solutions - Trading Framework
Trading Director - Orquestador Principal

Responsabilidades:
- Gestionar loop principal del sistema
- Despachar eventos a los handlers correspondientes
- Coordinar flujo entre módulos
- Controlar ciclo de vida del sistema
"""

from core.events.events import (
    DataEvent, SignalEvent, SizingEvent, OrderEvent,
    ExecutionEvent, PlacedPendingOrderEvent
)
from core.utils.utils import Utils
from modules.data_provider.data_provider import DataProvider
from modules.signal_generator.signal_generator import SignalGenerator
from modules.position_sizer.position_sizer import PositionSizer
from modules.risk_manager.risk_manager import RiskManager
from modules.order_executor.order_executor import OrderExecutor
from modules.notifications.notifications import NotificationService
from queue import Queue, Empty
from typing import Dict, Callable, Any
import time


class TradingDirector:
    """
    Orquestador central del framework de trading.
    Implementa el patrón Event-Driven Architecture.
    """
    
    def __init__(
        self,
        events_queue: Queue,
        data_provider: DataProvider,
        signal_generator: SignalGenerator,
        position_sizer: PositionSizer,
        risk_manager: RiskManager,
        order_executor: OrderExecutor,
        notification_service: NotificationService
    ):
        """
        Inicializa el Trading Director con todos los módulos.
        
        Args:
            events_queue: Cola central de eventos
            data_provider: Proveedor de datos de mercado
            signal_generator: Generador de señales
            position_sizer: Calculador de tamaño de posición
            risk_manager: Gestor de riesgo
            order_executor: Ejecutor de órdenes
            notification_service: Servicio de notificaciones
        """
        self.events_queue = events_queue
        
        # Referencias a módulos
        self.DATA_PROVIDER = data_provider
        self.SIGNAL_GENERATOR = signal_generator
        self.POSITION_SIZER = position_sizer
        self.RISK_MANAGER = risk_manager
        self.ORDER_EXECUTOR = order_executor
        self.NOTIFICATIONS = notification_service
        
        # Control de ejecución
        self.continue_trading = True
        
        # Mapeo de eventos a handlers
        self.event_handlers: Dict[str, Callable] = {
            "DATA": self._handle_data_event,
            "SIGNAL": self._handle_signal_event,
            "SIZING": self._handle_sizing_event,
            "ORDER": self._handle_order_event,
            "EXECUTION": self._handle_execution_event,
            "PENDING": self._handle_pending_order_event
        }
        
        print(f"\n{Utils.dateprint()} - ✓ Trading Director inicializado")
        print(f"{'='*60}")
        print("SISTEMA LISTO PARA OPERAR")
        print(f"{'='*60}\n")
    
    
    # ========================================================================
    # EVENT HANDLERS
    # ========================================================================
    
    def _handle_data_event(self, event: DataEvent) -> None:
        """
        Procesa eventos de nuevos datos de mercado.
        
        Flujo:
        DataEvent → Signal Generator
        
        Args:
            event: Evento con nuevos datos OHLCV
        """
        symbol = event.symbol
        close_price = event.data['close']
        
        print(
            f"{Utils.dateprint()} - 📊 DATA: {symbol} | "
            f"Close: {close_price:.5f}"
        )
        
        # Pasar al generador de señales
        self.SIGNAL_GENERATOR.generate_signal(event)
    
    
    def _handle_signal_event(self, event: SignalEvent) -> None:
        """
        Procesa eventos de señales de trading.
        
        Flujo:
        SignalEvent → Position Sizer
        
        Args:
            event: Señal de trading generada
        """
        print(
            f"{Utils.dateprint()} - 🎯 SIGNAL: {event.signal} {event.symbol} | "
            f"Tipo: {event.target_order}"
        )
        
        # Pasar al position sizer
        self.POSITION_SIZER.size_signal(event)
    
    
    def _handle_sizing_event(self, event: SizingEvent) -> None:
        """
        Procesa eventos con tamaño de posición calculado.
        
        Flujo:
        SizingEvent → Risk Manager
        
        Args:
            event: Evento con volumen calculado
        """
        print(
            f"{Utils.dateprint()} - 📏 SIZING: {event.signal} {event.symbol} | "
            f"Volumen: {event.volume}"
        )
        
        # Pasar al risk manager
        self.RISK_MANAGER.assess_order(event)
    
    
    def _handle_order_event(self, event: OrderEvent) -> None:
        """
        Procesa eventos de órdenes aprobadas por risk.
        
        Flujo:
        OrderEvent → Order Executor
        
        Args:
            event: Orden lista para ejecutar
        """
        print(
            f"{Utils.dateprint()} - 📋 ORDER: {event.signal} {event.symbol} | "
            f"Volumen: {event.volume}"
        )
        
        # Ejecutar orden
        self.ORDER_EXECUTOR.execute_order(event)
    
    
    def _handle_execution_event(self, event: ExecutionEvent) -> None:
        """
        Procesa eventos de ejecución exitosa.
        
        Args:
            event: Evento de ejecución completada
        """
        message = (
            f"Ejecución: {event.signal} {event.symbol}\n"
            f"Volumen: {event.volume}\n"
            f"Precio: {event.fill_price}\n"
            f"Hora: {event.fill_time}"
        )
        
        print(
            f"{Utils.dateprint()} - 💰 EXECUTION: {event.signal} {event.symbol} | "
            f"Vol: {event.volume} | Precio: {event.fill_price}"
        )
        
        # Enviar notificación
        self.NOTIFICATIONS.send_notification(
            title=f"MARKET ORDER - {event.symbol}",
            message=message
        )
    
    
    def _handle_pending_order_event(self, event: PlacedPendingOrderEvent) -> None:
        """
        Procesa eventos de órdenes pending colocadas.
        
        Args:
            event: Evento de pending order colocada
        """
        message = (
            f"Orden Pending: {event.signal} {event.target_order} {event.symbol}\n"
            f"Volumen: {event.volume}\n"
            f"Precio: {event.target_price}\n"
            f"SL: {event.sl} | TP: {event.tp}"
        )
        
        print(
            f"{Utils.dateprint()} - 📌 PENDING: {event.signal} {event.target_order} "
            f"{event.symbol} | Precio: {event.target_price}"
        )
        
        # Enviar notificación
        self.NOTIFICATIONS.send_notification(
            title=f"PENDING ORDER - {event.symbol}",
            message=message
        )
    
    
    def _handle_unknown_event(self, event: Any) -> None:
        """
        Maneja eventos desconocidos (error crítico).
        
        Args:
            event: Evento no reconocido
        """
        print(
            f"{Utils.dateprint()} - ❌ ERROR CRÍTICO: "
            f"Evento desconocido recibido: {event}"
        )
        self.continue_trading = False
    
    
    def _handle_none_event(self, event: None) -> None:
        """
        Maneja eventos nulos (error crítico).
        
        Args:
            event: Evento nulo
        """
        print(f"{Utils.dateprint()} - ❌ ERROR CRÍTICO: Evento nulo recibido")
        self.continue_trading = False
    
    
    # ========================================================================
    # MAIN EXECUTION LOOP
    # ========================================================================
    
    def execute(self) -> None:
        """
        Loop principal del sistema de trading.
        
        Ciclo:
        1. Intentar obtener evento de la cola
        2. Si hay evento → procesarlo con handler correspondiente
        3. Si no hay evento → verificar nuevos datos de mercado
        4. Repetir hasta interrupción
        
        La velocidad del loop está controlada por sleep() al final.
        """
        print(f"{Utils.dateprint()} - ▶️ Iniciando loop principal...\n")
        
        try:
            while self.continue_trading:
                try:
                    # Intentar obtener evento (non-blocking)
                    event = self.events_queue.get(block=False)
                    
                    if event is not None:
                        # Obtener handler apropiado
                        handler = self.event_handlers.get(
                            event.event_type,
                            self._handle_unknown_event
                        )
                        
                        # Procesar evento
                        handler(event)
                    else:
                        self._handle_none_event(event)
                
                except Empty:
                    # No hay eventos en cola → verificar nuevos datos
                    self.DATA_PROVIDER.check_for_new_data()
                
                # Control de frecuencia del loop
                time.sleep(0.01)  # 10ms entre iteraciones
        
        except KeyboardInterrupt:
            print(f"\n{Utils.dateprint()} - ⚠️ Interrupción manual detectada")
        
        finally:
            print(f"\n{Utils.dateprint()} - 🛑 Sistema detenido")
            print(f"{'='*60}\n")
