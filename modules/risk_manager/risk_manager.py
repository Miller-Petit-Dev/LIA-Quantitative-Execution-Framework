"""
LIA Engineering Solutions - Trading Framework
Risk Manager - Gestor de Riesgo

Valida que las operaciones cumplan con límites de riesgo establecidos.
Implementa control por máximo leverage factor.
"""

from core.events.events import SizingEvent, OrderEvent
from core.utils.utils import Utils
from modules.data_provider.data_provider import DataProvider
from modules.portfolio.portfolio import Portfolio
from queue import Queue
import MetaTrader5 as mt5
import sys


class RiskManager:
    """
    Valida operaciones contra límites de riesgo definidos.
    """
    
    def __init__(
        self,
        events_queue: Queue,
        data_provider: DataProvider,
        portfolio: Portfolio,
        max_leverage_factor: float = 3.0
    ):
        """
        Inicializa el risk manager.
        
        Args:
            events_queue: Cola de eventos del sistema
            data_provider: Proveedor de datos de mercado
            portfolio: Gestor de portfolio
            max_leverage_factor: Máximo factor de apalancamiento permitido
                Ej: 3.0 = exposición máxima de 3x el equity
        """
        self.events_queue = events_queue
        self.DATA_PROVIDER = data_provider
        self.PORTFOLIO = portfolio
        self.max_leverage_factor = max_leverage_factor
        
        print(
            f"{Utils.dateprint()} - ✓ Risk Manager inicializado: "
            f"Max Leverage Factor = {max_leverage_factor}x"
        )
    
    
    def _compute_value_of_position_in_account_currency(
        self,
        symbol: str,
        volume: float,
        position_type: int
    ) -> float:
        """
        Calcula el valor de una posición en la divisa de la cuenta.
        
        Args:
            symbol: Símbolo de la posición
            volume: Volumen en lotes
            position_type: mt5.ORDER_TYPE_BUY o mt5.ORDER_TYPE_SELL
            
        Returns:
            Valor de la posición en divisa de cuenta
        """
        symbol_info = mt5.symbol_info(symbol)
        account_currency = mt5.account_info().currency
        
        # Unidades operadas
        traded_units = volume * symbol_info.trade_contract_size
        
        # Valor en divisa profit del símbolo
        tick = self.DATA_PROVIDER.get_latest_tick(symbol)
        price = tick.get('bid', 0.0)
        value_in_profit_ccy = traded_units * price
        
        # Convertir a divisa de cuenta
        value_in_account_ccy = Utils.convert_currency_amount_to_another_currency(
            value_in_profit_ccy,
            symbol_info.currency_profit,
            account_currency
        )
        
        # Invertir signo para posiciones cortas
        if position_type == mt5.ORDER_TYPE_SELL:
            return -value_in_account_ccy
        else:
            return value_in_account_ccy
    
    
    def _compute_current_positions_value(self) -> float:
        """
        Calcula el valor total de posiciones abiertas en divisa de cuenta.
        
        Returns:
            Valor total de exposición actual
        """
        positions = self.PORTFOLIO.get_strategy_open_positions()
        
        total_value = 0.0
        for position in positions:
            value = self._compute_value_of_position_in_account_currency(
                position.symbol,
                position.volume,
                position.type
            )
            total_value += value
        
        return total_value
    
    
    def _compute_leverage_factor(self, account_value: float) -> float:
        """
        Calcula el leverage factor actual o proyectado.
        
        Args:
            account_value: Valor total de posiciones
            
        Returns:
            Factor de apalancamiento (exposición / equity)
        """
        equity = mt5.account_info().equity
        
        if equity <= 0:
            return sys.float_info.max  # Leverage infinito si no hay equity
        
        return abs(account_value) / equity
    
    
    def assess_order(self, sizing_event: SizingEvent) -> None:
        """
        Valida una orden contra límites de riesgo.
        
        Si pasa la validación, genera OrderEvent.
        Si no pasa, rechaza la orden (no genera evento).
        
        Args:
            sizing_event: Evento con sizing calculado
        """
        symbol = sizing_event.symbol
        volume = sizing_event.volume
        
        # Calcular exposición actual
        current_value = self._compute_current_positions_value()
        
        # Calcular valor de nueva posición
        position_type = (
            mt5.ORDER_TYPE_BUY if sizing_event.signal == "BUY"
            else mt5.ORDER_TYPE_SELL
        )
        new_position_value = self._compute_value_of_position_in_account_currency(
            symbol, volume, position_type
        )
        
        # Proyectar nuevo leverage
        projected_value = current_value + new_position_value
        projected_leverage = self._compute_leverage_factor(projected_value)
        
        # Validar leverage
        if projected_leverage <= self.max_leverage_factor:
            # APROBADO: Crear OrderEvent
            order_event = OrderEvent(
                symbol=sizing_event.symbol,
                signal=sizing_event.signal,
                target_order=sizing_event.target_order,
                target_price=sizing_event.target_price,
                magic_number=sizing_event.magic_number,
                sl=sizing_event.sl,
                tp=sizing_event.tp,
                volume=sizing_event.volume
            )
            
            self.events_queue.put(order_event)
            
            print(
                f"{Utils.dateprint()} - ✅ RISK CHECK PASSED: {sizing_event.signal} {symbol} "
                f"| Leverage proyectado: {projected_leverage:.2f}x "
                f"(max: {self.max_leverage_factor}x)"
            )
        else:
            # RECHAZADO: Excede leverage máximo
            print(
                f"{Utils.dateprint()} - ⚠️ RISK CHECK FAILED: {sizing_event.signal} {symbol} "
                f"| Leverage proyectado: {projected_leverage:.2f}x "
                f"EXCEDE máximo de {self.max_leverage_factor}x - ORDEN RECHAZADA"
            )
