"""
LIA Engineering Solutions - Trading Framework
Portfolio - Gestión de Posiciones

Responsabilidades:
- Consultar posiciones abiertas
- Filtrar posiciones por estrategia (magic number)
- Proveer información de posiciones por símbolo
"""

import MetaTrader5 as mt5
from typing import Dict, Tuple


class Portfolio:
    """
    Gestiona el acceso a posiciones abiertas y su información.
    """
    
    def __init__(self, magic_number: int):
        """
        Inicializa el portfolio con un magic number único.
        
        Args:
            magic_number: Identificador único de la estrategia
        """
        self.magic = magic_number
    
    
    def get_open_positions(self) -> Tuple:
        """
        Obtiene TODAS las posiciones abiertas en la cuenta.
        
        Returns:
            Tupla con objetos TradePosition de MT5
        """
        positions = mt5.positions_get()
        return positions if positions is not None else tuple()
    
    
    def get_strategy_open_positions(self) -> Tuple:
        """
        Obtiene solo las posiciones abiertas por esta estrategia.
        
        Returns:
            Tupla con posiciones que coinciden con el magic number
        """
        all_positions = self.get_open_positions()
        
        strategy_positions = [
            pos for pos in all_positions 
            if pos.magic == self.magic
        ]
        
        return tuple(strategy_positions)
    
    
    def get_number_of_open_positions_by_symbol(self, symbol: str) -> Dict[str, int]:
        """
        Cuenta posiciones abiertas de un símbolo (todas las estrategias).
        
        Args:
            symbol: Símbolo a consultar
            
        Returns:
            Diccionario con contadores:
                - LONG: Posiciones de compra
                - SHORT: Posiciones de venta
                - TOTAL: Total de posiciones
        """
        positions = mt5.positions_get(symbol=symbol)
        
        if positions is None:
            return {"LONG": 0, "SHORT": 0, "TOTAL": 0}
        
        longs = sum(1 for pos in positions if pos.type == mt5.ORDER_TYPE_BUY)
        shorts = sum(1 for pos in positions if pos.type == mt5.ORDER_TYPE_SELL)
        
        return {
            "LONG": longs,
            "SHORT": shorts,
            "TOTAL": longs + shorts
        }
    
    
    def get_number_of_strategy_open_positions_by_symbol(
        self, 
        symbol: str
    ) -> Dict[str, int]:
        """
        Cuenta posiciones abiertas de un símbolo por esta estrategia.
        
        Args:
            symbol: Símbolo a consultar
            
        Returns:
            Diccionario con contadores (solo de esta estrategia)
        """
        positions = mt5.positions_get(symbol=symbol)
        
        if positions is None:
            return {"LONG": 0, "SHORT": 0, "TOTAL": 0}
        
        # Filtrar por magic number
        strategy_positions = [pos for pos in positions if pos.magic == self.magic]
        
        longs = sum(1 for pos in strategy_positions if pos.type == mt5.ORDER_TYPE_BUY)
        shorts = sum(1 for pos in strategy_positions if pos.type == mt5.ORDER_TYPE_SELL)
        
        return {
            "LONG": longs,
            "SHORT": shorts,
            "TOTAL": longs + shorts
        }
    
    
    def has_open_position(self, symbol: str, direction: str = None) -> bool:
        """
        Verifica si hay posiciones abiertas para un símbolo.
        
        Args:
            symbol: Símbolo a verificar
            direction: 'LONG', 'SHORT' o None (cualquiera)
            
        Returns:
            True si hay al menos una posición abierta
        """
        counts = self.get_number_of_strategy_open_positions_by_symbol(symbol)
        
        if direction is None:
            return counts["TOTAL"] > 0
        elif direction.upper() == "LONG":
            return counts["LONG"] > 0
        elif direction.upper() == "SHORT":
            return counts["SHORT"] > 0
        else:
            return False
