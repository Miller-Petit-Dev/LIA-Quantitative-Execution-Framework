"""
LIA Engineering Solutions - Trading Framework
Platform Connector - Conexión con MetaTrader 5

Responsabilidades:
- Inicializar conexión con MT5
- Validar configuración de cuenta
- Verificar trading algorítmico habilitado
- Gestionar símbolos en MarketWatch
"""

import MetaTrader5 as mt5
import os
from dotenv import load_dotenv, find_dotenv
from core.utils.utils import Utils
from typing import List


class PlatformConnector:
    """
    Gestiona la conexión y configuración inicial con MetaTrader 5.
    """
    
    def __init__(self, symbol_list: List[str]):
        """
        Inicializa la conexión con MT5 y configura el entorno.
        
        Args:
            symbol_list: Lista de símbolos a operar
            
        Raises:
            Exception: Si falla la inicialización de MT5
        """
        # Cargar variables de entorno
        load_dotenv(find_dotenv())
        
        # Secuencia de inicialización
        self._initialize_platform()
        self._validate_account_type()
        self._print_account_info()
        self._check_algo_trading_enabled()
        self._add_symbols_to_marketwatch(symbol_list)
        
        print(f"{Utils.dateprint()} - ✓ Platform Connector inicializado correctamente\n")
    
    
    def _initialize_platform(self) -> None:
        """
        Inicializa la plataforma MT5 con credenciales del .env
        
        Variables de entorno requeridas:
            - MT5_PATH: Ruta al ejecutable de MT5
            - MT5_LOGIN: Número de cuenta
            - MT5_PASSWORD: Contraseña de la cuenta
            - MT5_SERVER: Servidor del broker
            - MT5_TIMEOUT: Timeout de conexión (ms)
            - MT5_PORTABLE: Modo portable (True/False)
            
        Raises:
            Exception: Si falla la inicialización
        """
        success = mt5.initialize(
            path=os.getenv("MT5_PATH"),
            login=int(os.getenv("MT5_LOGIN", "0")),
            password=os.getenv("MT5_PASSWORD"),
            server=os.getenv("MT5_SERVER"),
            timeout=int(os.getenv("MT5_TIMEOUT", "60000")),
            portable=eval(os.getenv("MT5_PORTABLE", "False"))
        )
        
        if success:
            print(f"{Utils.dateprint()} - ✓ Plataforma MT5 inicializada")
        else:
            error = mt5.last_error()
            raise Exception(
                f"Error al inicializar MT5: {error}. "
                "Verifica las credenciales en el archivo .env"
            )
    
    
    def _validate_account_type(self) -> None:
        """
        Valida el tipo de cuenta y advierte si es cuenta real.
        
        Tipos de cuenta:
            - DEMO: Cuenta de demostración (seguro)
            - REAL: Cuenta real (requiere confirmación)
            - CONTEST: Cuenta de concurso
            
        Raises:
            Exception: Si el usuario cancela operación en cuenta real
        """
        account_info = mt5.account_info()
        
        if account_info.trade_mode == mt5.ACCOUNT_TRADE_MODE_DEMO:
            print(f"{Utils.dateprint()} - ℹ Tipo de cuenta: DEMO")
            
        elif account_info.trade_mode == mt5.ACCOUNT_TRADE_MODE_REAL:
            print(f"\n{'='*60}")
            print("⚠️  ALERTA: CUENTA REAL DETECTADA")
            print("⚠️  CAPITAL EN RIESGO")
            print(f"{'='*60}\n")
            
            response = input("¿Deseas continuar operando en cuenta REAL? (y/n): ")
            
            if response.lower() != "y":
                mt5.shutdown()
                raise Exception("Operación cancelada por el usuario")
                
            print(f"{Utils.dateprint()} - ⚠️  Operando en cuenta REAL\n")
            
        else:
            print(f"{Utils.dateprint()} - ℹ Tipo de cuenta: CONCURSO")
    
    
    def _check_algo_trading_enabled(self) -> None:
        """
        Verifica que el trading algorítmico esté habilitado en MT5.
        
        Raises:
            Exception: Si el trading algorítmico está deshabilitado
        """
        if not mt5.terminal_info().trade_allowed:
            raise Exception(
                "Trading algorítmico DESHABILITADO. "
                "Por favor, habilítalo manualmente en MT5: "
                "Herramientas -> Opciones -> Expert Advisors -> "
                "'Permitir trading algorítmico'"
            )
        
        print(f"{Utils.dateprint()} - ✓ Trading algorítmico habilitado")
    
    
    def _add_symbols_to_marketwatch(self, symbols: List[str]) -> None:
        """
        Agrega símbolos al MarketWatch si no están visibles.
        
        Args:
            symbols: Lista de símbolos a agregar
        """
        print(f"\n{Utils.dateprint()} - Configurando símbolos en MarketWatch:")
        
        for symbol in symbols:
            # Verificar que el símbolo exista
            symbol_info = mt5.symbol_info(symbol)
            
            if symbol_info is None:
                print(
                    f"{Utils.dateprint()} - ✗ {symbol}: No existe o no disponible. "
                    f"MT5 error: {mt5.last_error()}"
                )
                continue
            
            # Agregar al MarketWatch si no está visible
            if not symbol_info.visible:
                if mt5.symbol_select(symbol, True):
                    print(f"{Utils.dateprint()} - ✓ {symbol}: Agregado a MarketWatch")
                else:
                    print(
                        f"{Utils.dateprint()} - ✗ {symbol}: Error al agregar. "
                        f"MT5 error: {mt5.last_error()}"
                    )
            else:
                print(f"{Utils.dateprint()} - ℹ {symbol}: Ya estaba en MarketWatch")
    
    
    def _print_account_info(self) -> None:
        """
        Muestra información detallada de la cuenta conectada.
        """
        account = mt5.account_info()._asdict()
        
        print(f"\n{'-'*60}")
        print("INFORMACIÓN DE LA CUENTA")
        print(f"{'-'*60}")
        print(f"ID Cuenta:     {account['login']}")
        print(f"Nombre:        {account['name']}")
        print(f"Broker:        {account['company']}")
        print(f"Servidor:      {account['server']}")
        print(f"Apalancamiento: 1:{account['leverage']}")
        print(f"Divisa:        {account['currency']}")
        print(f"Balance:       {account['balance']:.2f} {account['currency']}")
        print(f"Equity:        {account['equity']:.2f} {account['currency']}")
        print(f"{'-'*60}\n")
