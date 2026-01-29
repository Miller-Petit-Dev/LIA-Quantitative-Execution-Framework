"""
LIA Engineering Solutions - Trading Framework
Utilidades Comunes

Funciones auxiliares reutilizables en todo el framework.
"""

import MetaTrader5 as mt5
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional


class Utils:
    """
    Clase de utilidades estáticas para operaciones comunes.
    """
    
    @staticmethod
    def dateprint(timezone: str = "America/Argentina/Buenos_Aires") -> str:
        """
        Retorna timestamp formateado para logs.
        
        Args:
            timezone: Zona horaria (default: Buenos Aires)
            
        Returns:
            String con formato: dd/mm/yyyy HH:MM:SS.mmm
        """
        return datetime.now(ZoneInfo(timezone)).strftime("%d/%m/%Y %H:%M:%S.%f")[:-3]
    
    
    @staticmethod
    def convert_currency_amount_to_another_currency(
        amount: float, 
        from_ccy: str, 
        to_ccy: str
    ) -> float:
        """
        Convierte un monto de una divisa a otra usando tasas de MT5.
        
        Args:
            amount: Monto a convertir
            from_ccy: Divisa origen
            to_ccy: Divisa destino
            
        Returns:
            Monto convertido a la divisa destino
            
        Raises:
            Exception: Si el símbolo FX no está disponible
        """
        # Si las divisas son iguales, no hay conversión
        if from_ccy.upper() == to_ccy.upper():
            return amount
        
        # Símbolos FX principales disponibles
        all_fx_symbols = (
            "AUDCAD", "AUDCHF", "AUDJPY", "AUDNZD", "AUDUSD", 
            "CADCHF", "CADJPY", "CHFJPY", 
            "EURAUD", "EURCAD", "EURCHF", "EURGBP", "EURJPY", "EURNZD", "EURUSD",
            "GBPAUD", "GBPCAD", "GBPCHF", "GBPJPY", "GBPNZD", "GBPUSD",
            "NZDCAD", "NZDCHF", "NZDJPY", "NZDUSD",
            "USDCAD", "USDCHF", "USDJPY", "USDSEK", "USDNOK"
        )
        
        from_ccy = from_ccy.upper()
        to_ccy = to_ccy.upper()
        
        # Buscar símbolo que relacione ambas divisas
        try:
            fx_symbol = [
                symbol for symbol in all_fx_symbols 
                if from_ccy in symbol and to_ccy in symbol
            ][0]
        except IndexError:
            raise Exception(
                f"No se encontró símbolo FX para convertir {from_ccy} a {to_ccy}"
            )
        
        # Identificar divisa base del par
        fx_symbol_base = fx_symbol[:3]
        
        # Obtener último precio disponible
        try:
            tick = mt5.symbol_info_tick(fx_symbol)
            if tick is None:
                raise Exception(
                    f"Símbolo {fx_symbol} no disponible en MT5. "
                    "Verifica símbolos disponibles con tu broker."
                )
        except Exception as e:
            print(
                f"{Utils.dateprint()} - ERROR: No se pudo obtener tick de {fx_symbol}. "
                f"MT5 error: {mt5.last_error()}, Exception: {e}"
            )
            return 0.0
        
        last_price = tick.bid
        
        # Realizar conversión según configuración del par
        if fx_symbol_base == to_ccy:
            converted_amount = amount / last_price
        else:
            converted_amount = amount * last_price
            
        return converted_amount


    @staticmethod
    def format_trade_log(
        action: str, 
        symbol: str, 
        volume: float, 
        price: Optional[float] = None,
        additional_info: str = ""
    ) -> str:
        """
        Formatea mensajes de log para operaciones de trading.
        
        Args:
            action: Acción realizada (ej: "MARKET BUY", "PENDING SELL LIMIT")
            symbol: Símbolo operado
            volume: Volumen de la operación
            price: Precio de ejecución (opcional)
            additional_info: Información adicional (opcional)
            
        Returns:
            String formateado para log
        """
        msg = f"{Utils.dateprint()} - {action} | {symbol} | Vol: {volume}"
        
        if price:
            msg += f" | Precio: {price}"
            
        if additional_info:
            msg += f" | {additional_info}"
            
        return msg


    @staticmethod
    def validate_symbol_info(symbol: str) -> bool:
        """
        Valida que un símbolo esté disponible y visible en MT5.
        
        Args:
            symbol: Símbolo a validar
            
        Returns:
            True si el símbolo es válido y está visible
        """
        symbol_info = mt5.symbol_info(symbol)
        
        if symbol_info is None:
            print(
                f"{Utils.dateprint()} - ERROR: Símbolo {symbol} no existe "
                f"o no está disponible. MT5 error: {mt5.last_error()}"
            )
            return False
            
        if not symbol_info.visible:
            print(
                f"{Utils.dateprint()} - WARNING: Símbolo {symbol} no está "
                "visible en MarketWatch"
            )
            return False
            
        return True
