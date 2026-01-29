"""
LIA Engineering Solutions - Trading Framework
Main Application - Aplicación Principal

Este es el punto de entrada del sistema de trading.
Inicializa todos los módulos y ejecuta el Trading Director.
"""

from queue import Queue
import sys

# Módulos del framework
from modules.platform_connector.platform_connector import PlatformConnector
from modules.data_provider.data_provider import DataProvider
from modules.portfolio.portfolio import Portfolio
from modules.signal_generator.signal_generator import SignalGenerator
from modules.position_sizer.position_sizer import PositionSizer
from modules.risk_manager.risk_manager import RiskManager
from modules.order_executor.order_executor import OrderExecutor
from modules.notifications.notifications import NotificationService
from modules.trading_director.trading_director import TradingDirector

# Configuración
from config.trading_config import get_default_config, TradingConfig

# Utilidades
from core.utils.utils import Utils


def main():
    """
    Función principal del sistema.
    Orquesta la inicialización y ejecución del framework.
    """
    
    print("\n" + "="*60)
    print("LIA ENGINEERING SOLUTIONS")
    print("TRADING FRAMEWORK - EVENT-DRIVEN ARCHITECTURE")
    print("="*60 + "\n")
    
    try:
        # ====================================================================
        # CARGAR CONFIGURACIÓN
        # ====================================================================
        
        print(f"{Utils.dateprint()} - Cargando configuración...\n")
        
        # Opción 1: Usar configuración por defecto
        config = get_default_config()
        
        # Opción 2: Configuración personalizada
        # config = TradingConfig(
        #     symbols=['EURUSD', 'GBPUSD'],
        #     timeframe='5min',
        #     rsi_period=14,
        #     rsi_upper=70.0,
        #     rsi_lower=30.0,
        #     sl_points=100,
        #     tp_points=200,
        #     fixed_volume=0.05,
        #     max_leverage_factor=5.0,
        #     telegram_enabled=False
        # )
        
        print(f"✓ Configuración cargada:")
        print(f"  - Símbolos: {', '.join(config.symbols)}")
        print(f"  - Timeframe: {config.timeframe}")
        print(f"  - RSI: Period={config.rsi_period}, "
              f"Upper={config.rsi_upper}, Lower={config.rsi_lower}")
        print(f"  - SL/TP: {config.sl_points}/{config.tp_points} puntos")
        print(f"  - Volumen: {config.fixed_volume} lotes")
        print(f"  - Max Leverage: {config.max_leverage_factor}x\n")
        
        
        # ====================================================================
        # INICIALIZAR COLA DE EVENTOS
        # ====================================================================
        
        events_queue = Queue()
        print(f"{Utils.dateprint()} - ✓ Cola de eventos inicializada\n")
        
        
        # ====================================================================
        # INICIALIZAR MÓDULOS DEL FRAMEWORK
        # ====================================================================
        
        print(f"{Utils.dateprint()} - Inicializando módulos del framework...\n")
        
        # 1. Conectar con plataforma MT5
        platform = PlatformConnector(symbol_list=config.symbols)
        
        # 2. Proveedor de datos
        data_provider = DataProvider(
            events_queue=events_queue,
            symbol_list=config.symbols,
            timeframe=config.timeframe
        )
        
        # 3. Portfolio
        portfolio = Portfolio(magic_number=config.magic_number)
        print(f"{Utils.dateprint()} - ✓ Portfolio inicializado (Magic: {config.magic_number})")
        
        # 4. Order Executor
        order_executor = OrderExecutor(
            events_queue=events_queue,
            portfolio=portfolio
        )
        
        # 5. Signal Generator
        signal_generator = SignalGenerator(
            events_queue=events_queue,
            data_provider=data_provider,
            portfolio=portfolio,
            order_executor=order_executor,
            magic_number=config.magic_number,
            timeframe=config.timeframe,
            rsi_period=config.rsi_period,
            rsi_upper=config.rsi_upper,
            rsi_lower=config.rsi_lower,
            sl_points=config.sl_points,
            tp_points=config.tp_points
        )
        
        # 6. Position Sizer
        position_sizer = PositionSizer(
            events_queue=events_queue,
            fixed_volume=config.fixed_volume
        )
        
        # 7. Risk Manager
        risk_manager = RiskManager(
            events_queue=events_queue,
            data_provider=data_provider,
            portfolio=portfolio,
            max_leverage_factor=config.max_leverage_factor
        )
        
        # 8. Notification Service
        notifications = NotificationService(
            telegram_enabled=config.telegram_enabled,
            telegram_token=config.telegram_token,
            telegram_chat_id=config.telegram_chat_id
        )
        
        
        # ====================================================================
        # INICIALIZAR Y EJECUTAR TRADING DIRECTOR
        # ====================================================================
        
        trading_director = TradingDirector(
            events_queue=events_queue,
            data_provider=data_provider,
            signal_generator=signal_generator,
            position_sizer=position_sizer,
            risk_manager=risk_manager,
            order_executor=order_executor,
            notification_service=notifications
        )
        
        # Ejecutar loop principal
        trading_director.execute()
    
    
    except KeyboardInterrupt:
        print(f"\n{Utils.dateprint()} - ⚠️ Interrupción manual (Ctrl+C)")
        sys.exit(0)
    
    except Exception as e:
        print(f"\n{Utils.dateprint()} - ❌ ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    finally:
        print(f"\n{Utils.dateprint()} - Sistema finalizado\n")


if __name__ == "__main__":
    main()
