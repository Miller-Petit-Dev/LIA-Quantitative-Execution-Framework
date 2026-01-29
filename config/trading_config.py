"""
LIA Engineering Solutions - Trading Framework
Configuración Principal

Define todos los parámetros operativos del sistema.
Centraliza configuración para facilitar ajustes.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class TradingConfig:
    """
    Configuración principal del sistema de trading.
    """
    
    # ========================================================================
    # SÍMBOLOS Y TIMEFRAME
    # ========================================================================
    
    symbols: List[str] = None
    """Lista de símbolos a operar (ej: ['EURUSD', 'GBPUSD'])"""
    
    timeframe: str = "1min"
    """Timeframe de operación (ej: '1min', '5min', '1h')"""
    
    
    # ========================================================================
    # IDENTIFICACIÓN DE ESTRATEGIA
    # ========================================================================
    
    magic_number: int = 12345
    """Magic number único para identificar trades de esta estrategia"""
    
    
    # ========================================================================
    # PARÁMETROS DE ESTRATEGIA (RSI)
    # ========================================================================
    
    rsi_period: int = 14
    """Período del indicador RSI"""
    
    rsi_upper: float = 70.0
    """Nivel de sobrecompra del RSI (señal SELL)"""
    
    rsi_lower: float = 30.0
    """Nivel de sobreventa del RSI (señal BUY)"""
    
    sl_points: int = 50
    """Stop Loss en puntos (0.0001 para pares no-JPY, 0.01 para JPY)"""
    
    tp_points: int = 100
    """Take Profit en puntos"""
    
    
    # ========================================================================
    # POSITION SIZING
    # ========================================================================
    
    fixed_volume: float = 0.01
    """Volumen fijo por operación en lotes"""
    
    
    # ========================================================================
    # RISK MANAGEMENT
    # ========================================================================
    
    max_leverage_factor: float = 3.0
    """
    Máximo factor de apalancamiento permitido.
    Ej: 3.0 = exposición máxima de 3x el equity
    """
    
    
    # ========================================================================
    # NOTIFICACIONES
    # ========================================================================
    
    telegram_enabled: bool = False
    """Habilitar notificaciones por Telegram"""
    
    telegram_token: str = None
    """Token del bot de Telegram (obtener de @BotFather)"""
    
    telegram_chat_id: str = None
    """Chat ID para recibir notificaciones"""
    
    
    def __post_init__(self):
        """Validación de configuración al inicializar."""
        
        # Validar símbolos
        if not self.symbols or len(self.symbols) == 0:
            raise ValueError("Debe especificar al menos un símbolo en 'symbols'")
        
        # Validar parámetros de RSI
        if self.rsi_period < 2:
            raise ValueError("rsi_period debe ser >= 2")
        
        if not (0 < self.rsi_lower < self.rsi_upper < 100):
            raise ValueError(
                "rsi_lower debe ser < rsi_upper, y ambos entre 0 y 100"
            )
        
        # Validar SL y TP
        if self.sl_points <= 0:
            raise ValueError("sl_points debe ser > 0")
        
        if self.tp_points <= 0:
            raise ValueError("tp_points debe ser > 0")
        
        # Validar volumen
        if self.fixed_volume <= 0:
            raise ValueError("fixed_volume debe ser > 0")
        
        # Validar leverage
        if self.max_leverage_factor <= 0:
            raise ValueError("max_leverage_factor debe ser > 0")
        
        # Validar Telegram
        if self.telegram_enabled:
            if not self.telegram_token or not self.telegram_chat_id:
                raise ValueError(
                    "Si telegram_enabled=True, debe proporcionar "
                    "telegram_token y telegram_chat_id"
                )


# ============================================================================
# CONFIGURACIÓN POR DEFECTO
# ============================================================================

def get_default_config() -> TradingConfig:
    """
    Retorna configuración por defecto del sistema.
    
    Returns:
        Instancia de TradingConfig con valores predeterminados
    """
    return TradingConfig(
        # Símbolos
        symbols=['EURUSD', 'GBPUSD', 'USDJPY'],
        timeframe='1min',
        
        # Estrategia
        magic_number=12345,
        
        # RSI
        rsi_period=14,
        rsi_upper=70.0,
        rsi_lower=30.0,
        sl_points=50,
        tp_points=100,
        
        # Sizing
        fixed_volume=0.01,
        
        # Risk
        max_leverage_factor=3.0,
        
        # Notifications
        telegram_enabled=False,
        telegram_token=None,
        telegram_chat_id=None
    )
