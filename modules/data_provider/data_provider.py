"""
LIA Engineering Solutions - Trading Framework
Data Provider - Proveedor de Datos de Mercado

Responsabilidades:
- Obtener datos OHLCV desde MT5
- Detectar nuevas barras cerradas
- Generar eventos de datos (DataEvent)
- Gestionar último timestamp por símbolo
"""

import MetaTrader5 as mt5
import pandas as pd
from typing import Dict, List
from datetime import datetime
from queue import Queue
from core.events.events import DataEvent
from core.utils.utils import Utils


class DataProvider:
    """
    Provee datos de mercado y genera eventos cuando hay nuevas barras.
    """
    
    # Mapeo de timeframes string a constantes MT5
    TIMEFRAME_MAP = {
        '1min': mt5.TIMEFRAME_M1,
        '2min': mt5.TIMEFRAME_M2,
        '3min': mt5.TIMEFRAME_M3,
        '4min': mt5.TIMEFRAME_M4,
        '5min': mt5.TIMEFRAME_M5,
        '6min': mt5.TIMEFRAME_M6,
        '10min': mt5.TIMEFRAME_M10,
        '12min': mt5.TIMEFRAME_M12,
        '15min': mt5.TIMEFRAME_M15,
        '20min': mt5.TIMEFRAME_M20,
        '30min': mt5.TIMEFRAME_M30,
        '1h': mt5.TIMEFRAME_H1,
        '2h': mt5.TIMEFRAME_H2,
        '3h': mt5.TIMEFRAME_H3,
        '4h': mt5.TIMEFRAME_H4,
        '6h': mt5.TIMEFRAME_H6,
        '8h': mt5.TIMEFRAME_H8,
        '12h': mt5.TIMEFRAME_H12,
        '1d': mt5.TIMEFRAME_D1,
        '1w': mt5.TIMEFRAME_W1,
        '1M': mt5.TIMEFRAME_MN1,
    }
    
    
    def __init__(self, events_queue: Queue, symbol_list: List[str], timeframe: str):
        """
        Inicializa el proveedor de datos.
        
        Args:
            events_queue: Cola de eventos del sistema
            symbol_list: Lista de símbolos a monitorear
            timeframe: Timeframe de las barras (ej: '1min', '5min', '1h')
        """
        self.events_queue = events_queue
        self.symbols = symbol_list
        self.timeframe = timeframe
        
        # Control de última barra vista por símbolo
        self.last_bar_datetime: Dict[str, datetime] = {
            symbol: datetime.min for symbol in self.symbols
        }
        
        print(f"{Utils.dateprint()} - ✓ Data Provider inicializado para {len(symbol_list)} símbolos")
    
    
    def _map_timeframe(self, timeframe: str) -> int:
        """
        Convierte timeframe string a constante MT5.
        
        Args:
            timeframe: Timeframe en formato string
            
        Returns:
            Constante MT5 correspondiente
            
        Raises:
            ValueError: Si el timeframe no es válido
        """
        if timeframe not in self.TIMEFRAME_MAP:
            raise ValueError(
                f"Timeframe '{timeframe}' no válido. "
                f"Opciones: {', '.join(self.TIMEFRAME_MAP.keys())}"
            )
        return self.TIMEFRAME_MAP[timeframe]
    
    
    def get_latest_closed_bar(self, symbol: str, timeframe: str) -> pd.Series:
        """
        Obtiene la última barra cerrada de un símbolo.
        
        Args:
            symbol: Símbolo a consultar
            timeframe: Timeframe de la barra
            
        Returns:
            Serie de pandas con datos OHLCV (vacía si hay error)
        """
        tf = self._map_timeframe(timeframe)
        from_position = 1  # Posición 1 = última barra CERRADA
        num_bars = 1
        
        try:
            # Obtener datos desde MT5
            bars_array = mt5.copy_rates_from_pos(symbol, tf, from_position, num_bars)
            
            if bars_array is None:
                print(
                    f"{Utils.dateprint()} - ERROR: No se pudieron obtener datos "
                    f"de {symbol}. MT5 error: {mt5.last_error()}"
                )
                return pd.Series()
            
            # Convertir a DataFrame
            bars = pd.DataFrame(bars_array)
            
            # Configurar índice temporal
            bars['time'] = pd.to_datetime(bars['time'], unit='s')
            bars.set_index('time', inplace=True)
            
            # Renombrar y reorganizar columnas
            bars.rename(
                columns={
                    'tick_volume': 'tickvol',
                    'real_volume': 'vol'
                },
                inplace=True
            )
            bars = bars[['open', 'high', 'low', 'close', 'tickvol', 'vol', 'spread']]
            
            # Retornar última fila como Serie
            return bars.iloc[-1] if not bars.empty else pd.Series()
            
        except Exception as e:
            print(
                f"{Utils.dateprint()} - ERROR: Excepción al obtener datos de "
                f"{symbol} {timeframe}. MT5 error: {mt5.last_error()}, Exception: {e}"
            )
            return pd.Series()
    
    
    def get_latest_closed_bars(
        self, 
        symbol: str, 
        timeframe: str, 
        num_bars: int = 100
    ) -> pd.DataFrame:
        """
        Obtiene múltiples barras cerradas de un símbolo.
        
        Args:
            symbol: Símbolo a consultar
            timeframe: Timeframe de las barras
            num_bars: Cantidad de barras a obtener
            
        Returns:
            DataFrame con datos OHLCV (vacío si hay error)
        """
        tf = self._map_timeframe(timeframe)
        from_position = 1
        bars_count = max(1, num_bars)
        
        try:
            bars_array = mt5.copy_rates_from_pos(symbol, tf, from_position, bars_count)
            
            if bars_array is None:
                print(
                    f"{Utils.dateprint()} - ERROR: No se pudieron obtener {num_bars} "
                    f"barras de {symbol}. MT5 error: {mt5.last_error()}"
                )
                return pd.DataFrame()
            
            bars = pd.DataFrame(bars_array)
            
            bars['time'] = pd.to_datetime(bars['time'], unit='s')
            bars.set_index('time', inplace=True)
            
            bars.rename(
                columns={
                    'tick_volume': 'tickvol',
                    'real_volume': 'vol'
                },
                inplace=True
            )
            bars = bars[['open', 'high', 'low', 'close', 'tickvol', 'vol', 'spread']]
            
            return bars
            
        except Exception as e:
            print(
                f"{Utils.dateprint()} - ERROR: Excepción al obtener {num_bars} barras "
                f"de {symbol} {timeframe}. MT5 error: {mt5.last_error()}, Exception: {e}"
            )
            return pd.DataFrame()
    
    
    def get_latest_tick(self, symbol: str) -> dict:
        """
        Obtiene el último tick (precio actual) de un símbolo.
        
        Args:
            symbol: Símbolo a consultar
            
        Returns:
            Diccionario con datos del tick (vacío si hay error)
        """
        try:
            tick = mt5.symbol_info_tick(symbol)
            
            if tick is None:
                print(
                    f"{Utils.dateprint()} - ERROR: No se pudo obtener tick de {symbol}. "
                    f"MT5 error: {mt5.last_error()}"
                )
                return {}
            
            return tick._asdict()
            
        except Exception as e:
            print(
                f"{Utils.dateprint()} - ERROR: Excepción al obtener tick de {symbol}. "
                f"MT5 error: {mt5.last_error()}, Exception: {e}"
            )
            return {}
    
    
    def check_for_new_data(self) -> None:
        """
        Verifica si hay nuevas barras cerradas para cada símbolo.
        Si detecta una nueva barra, genera un DataEvent y lo coloca en la cola.
        
        Este método se llama continuamente en el loop principal.
        """
        for symbol in self.symbols:
            latest_bar = self.get_latest_closed_bar(symbol, self.timeframe)
            
            # Validar que obtuvimos datos
            if latest_bar is None or latest_bar.empty:
                continue
            
            # Verificar si es una nueva barra
            if latest_bar.name > self.last_bar_datetime[symbol]:
                self.last_bar_datetime[symbol] = latest_bar.name
                
                # Generar y encolar evento
                data_event = DataEvent(symbol=symbol, data=latest_bar)
                self.events_queue.put(data_event)
