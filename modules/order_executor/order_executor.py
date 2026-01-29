"""
LIA Engineering Solutions - Trading Framework
Order Executor - Ejecutor de Órdenes

Responsabilidades:
- Ejecutar órdenes de mercado y pending
- Cerrar posiciones por ticket
- Generar ExecutionEvents
- Manejo de errores de ejecución
"""

from core.events.events import (
    OrderEvent, ExecutionEvent, PlacedPendingOrderEvent, SignalType
)
from core.utils.utils import Utils
from modules.portfolio.portfolio import Portfolio
from queue import Queue
import MetaTrader5 as mt5
import time
from datetime import datetime
import pandas as pd


class OrderExecutor:
    """
    Ejecuta órdenes en MetaTrader 5 y gestiona el ciclo de vida de trades.
    """
    
    def __init__(self, events_queue: Queue, portfolio: Portfolio):
        """
        Inicializa el order executor.
        
        Args:
            events_queue: Cola de eventos del sistema
            portfolio: Gestor de portfolio
        """
        self.events_queue = events_queue
        self.PORTFOLIO = portfolio
        
        print(f"{Utils.dateprint()} - ✓ Order Executor inicializado")
    
    
    def execute_order(self, order_event: OrderEvent) -> None:
        """
        Ejecuta una orden según su tipo (MARKET, LIMIT, STOP).
        
        Args:
            order_event: Evento con la orden a ejecutar
        """
        if order_event.target_order == "MARKET":
            self._execute_market_order(order_event)
        else:
            self._send_pending_order(order_event)
    
    
    def _execute_market_order(self, order_event: OrderEvent) -> None:
        """
        Ejecuta una orden a mercado (ejecución inmediata).
        
        Args:
            order_event: Orden a ejecutar
        """
        symbol = order_event.symbol
        signal = order_event.signal
        volume = order_event.volume
        
        # Determinar tipo de orden MT5
        order_type = (
            mt5.ORDER_TYPE_BUY if signal == "BUY"
            else mt5.ORDER_TYPE_SELL
        )
        
        # Obtener precio actual
        symbol_info = mt5.symbol_info(symbol)
        price = symbol_info.ask if signal == "BUY" else symbol_info.bid
        
        # Crear request
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "price": price,
            "sl": order_event.sl,
            "tp": order_event.tp,
            "type": order_type,
            "deviation": 10,  # Slippage permitido
            "magic": order_event.magic_number,
            "comment": "LIA Framework",
            "type_filling": mt5.ORDER_FILLING_FOK,
        }
        
        # Enviar orden
        result = mt5.order_send(request)
        
        # Procesar resultado
        if self._check_execution_status(result):
            print(
                f"{Utils.dateprint()} - ✅ MARKET ORDER EJECUTADA: "
                f"{signal} {symbol} | Vol: {volume} | Precio: {result.price}"
            )
            self._create_and_put_execution_event(result)
        else:
            print(
                f"{Utils.dateprint()} - ❌ ERROR MARKET ORDER: "
                f"{signal} {symbol} | {result.comment} (code: {result.retcode})"
            )
    
    
    def _send_pending_order(self, order_event: OrderEvent) -> None:
        """
        Coloca una orden pending (LIMIT o STOP).
        
        Args:
            order_event: Orden pending a colocar
        """
        symbol = order_event.symbol
        signal = order_event.signal
        target_order = order_event.target_order
        
        # Determinar tipo de orden pending
        if target_order == "STOP":
            order_type = (
                mt5.ORDER_TYPE_BUY_STOP if signal == "BUY"
                else mt5.ORDER_TYPE_SELL_STOP
            )
        elif target_order == "LIMIT":
            order_type = (
                mt5.ORDER_TYPE_BUY_LIMIT if signal == "BUY"
                else mt5.ORDER_TYPE_SELL_LIMIT
            )
        else:
            print(
                f"{Utils.dateprint()} - ERROR: Tipo de orden pending "
                f"'{target_order}' no válido"
            )
            return
        
        # Crear request
        request = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "volume": order_event.volume,
            "price": order_event.target_price,
            "sl": order_event.sl,
            "tp": order_event.tp,
            "type": order_type,
            "deviation": 0,
            "magic": order_event.magic_number,
            "comment": "LIA Framework Pending",
            "type_filling": mt5.ORDER_FILLING_FOK,
            "type_time": mt5.ORDER_TIME_GTC
        }
        
        # Enviar orden
        result = mt5.order_send(request)
        
        # Procesar resultado
        if self._check_execution_status(result):
            print(
                f"{Utils.dateprint()} - ✅ PENDING ORDER COLOCADA: "
                f"{signal} {target_order} {symbol} | "
                f"Vol: {order_event.volume} | Precio: {order_event.target_price}"
            )
            self._create_and_put_placed_pending_order_event(order_event)
        else:
            print(
                f"{Utils.dateprint()} - ❌ ERROR PENDING ORDER: "
                f"{signal} {target_order} {symbol} | "
                f"{result.comment} (code: {result.retcode})"
            )
    
    
    def close_position_by_ticket(self, ticket: int) -> None:
        """
        Cierra una posición por su ticket.
        
        Args:
            ticket: Ticket de la posición a cerrar
        """
        # Obtener posición
        positions = mt5.positions_get(ticket=ticket)
        
        if not positions:
            print(
                f"{Utils.dateprint()} - ERROR: No existe posición "
                f"con ticket {ticket}"
            )
            return
        
        position = positions[0]
        
        # Determinar tipo de cierre (inverso al de apertura)
        close_type = (
            mt5.ORDER_TYPE_SELL if position.type == mt5.ORDER_TYPE_BUY
            else mt5.ORDER_TYPE_BUY
        )
        
        # Obtener precio de cierre
        symbol_info = mt5.symbol_info(position.symbol)
        price = symbol_info.bid if close_type == mt5.ORDER_TYPE_SELL else symbol_info.ask
        
        # Crear request de cierre
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "position": position.ticket,
            "symbol": position.symbol,
            "volume": position.volume,
            "price": price,
            "type": close_type,
            "deviation": 10,
            "type_filling": mt5.ORDER_FILLING_FOK,
            "comment": "LIA Framework Close"
        }
        
        # Enviar orden de cierre
        result = mt5.order_send(request)
        
        # Procesar resultado
        if self._check_execution_status(result):
            print(
                f"{Utils.dateprint()} - ✅ POSICIÓN CERRADA: "
                f"Ticket {ticket} | {position.symbol} | Vol: {position.volume}"
            )
            self._create_and_put_execution_event(result)
        else:
            print(
                f"{Utils.dateprint()} - ❌ ERROR AL CERRAR: "
                f"Ticket {ticket} | {result.comment} (code: {result.retcode})"
            )
    
    
    def _check_execution_status(self, result) -> bool:
        """
        Verifica si una orden se ejecutó correctamente.
        
        Args:
            result: Resultado de mt5.order_send()
            
        Returns:
            True si la ejecución fue exitosa
        """
        return result.retcode in (
            mt5.TRADE_RETCODE_DONE,
            mt5.TRADE_RETCODE_DONE_PARTIAL
        )
    
    
    def _create_and_put_execution_event(self, result) -> None:
        """
        Crea un ExecutionEvent a partir del resultado de ejecución.
        
        Args:
            result: Resultado de mt5.order_send()
        """
        # Intentar obtener deal info
        deal = None
        fill_time = datetime.now()
        
        # Esperar a que MT5 genere el deal (hasta 5 intentos)
        for _ in range(5):
            time.sleep(0.5)
            try:
                deals = mt5.history_deals_get(position=result.order)
                if deals:
                    deal = deals[0]
                    break
            except:
                pass
        
        # Usar timestamp del deal si está disponible
        if deal:
            fill_time = pd.to_datetime(deal.time_msc, unit='ms')
        
        # Crear evento
        execution_event = ExecutionEvent(
            symbol=result.request.symbol,
            signal=SignalType.BUY if result.request.type == mt5.DEAL_TYPE_BUY else SignalType.SELL,
            fill_price=result.price,
            fill_time=fill_time,
            volume=result.request.volume
        )
        
        self.events_queue.put(execution_event)
    
    
    def _create_and_put_placed_pending_order_event(
        self,
        order_event: OrderEvent
    ) -> None:
        """
        Crea un PlacedPendingOrderEvent.
        
        Args:
            order_event: Orden pending que se colocó
        """
        pending_event = PlacedPendingOrderEvent(
            symbol=order_event.symbol,
            signal=order_event.signal,
            target_order=order_event.target_order,
            target_price=order_event.target_price,
            magic_number=order_event.magic_number,
            sl=order_event.sl,
            tp=order_event.tp,
            volume=order_event.volume
        )
        
        self.events_queue.put(pending_event)
