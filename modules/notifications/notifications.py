"""
LIA Engineering Solutions - Trading Framework
Notification Service - Sistema de Notificaciones

Soporta:
- Notificaciones por consola (siempre activo)
- Notificaciones por Telegram (opcional)
"""

from core.utils.utils import Utils
from typing import Optional
import asyncio


class NotificationService:
    """
    Gestiona el envío de notificaciones multi-canal.
    """
    
    def __init__(
        self,
        telegram_enabled: bool = False,
        telegram_token: Optional[str] = None,
        telegram_chat_id: Optional[str] = None
    ):
        """
        Inicializa el servicio de notificaciones.
        
        Args:
            telegram_enabled: Habilitar notificaciones por Telegram
            telegram_token: Token del bot de Telegram
            telegram_chat_id: Chat ID para enviar mensajes
        """
        self.telegram_enabled = telegram_enabled
        self.telegram_bot = None
        self.chat_id = telegram_chat_id
        
        # Inicializar Telegram si está habilitado
        if telegram_enabled and telegram_token and telegram_chat_id:
            try:
                import telegram
                self.telegram_bot = telegram.Bot(telegram_token)
                print(f"{Utils.dateprint()} - ✓ Notificaciones Telegram habilitadas")
            except ImportError:
                print(
                    f"{Utils.dateprint()} - WARNING: python-telegram-bot no instalado. "
                    "Solo se usarán notificaciones por consola."
                )
                self.telegram_enabled = False
            except Exception as e:
                print(
                    f"{Utils.dateprint()} - WARNING: Error al inicializar Telegram: {e}. "
                    "Solo se usarán notificaciones por consola."
                )
                self.telegram_enabled = False
        else:
            print(f"{Utils.dateprint()} - ℹ Notificaciones solo por consola")
    
    
    def send_notification(self, title: str, message: str) -> None:
        """
        Envía una notificación por todos los canales habilitados.
        
        Args:
            title: Título de la notificación
            message: Contenido del mensaje
        """
        # Notificación por consola (siempre activo)
        full_message = f"\n{'='*60}\n📢 {title}\n{'-'*60}\n{message}\n{'='*60}\n"
        print(full_message)
        
        # Notificación por Telegram (si está habilitado)
        if self.telegram_enabled and self.telegram_bot:
            try:
                asyncio.run(self._send_telegram_message(title, message))
            except Exception as e:
                print(f"{Utils.dateprint()} - ERROR al enviar Telegram: {e}")
    
    
    async def _send_telegram_message(self, title: str, message: str) -> None:
        """
        Envía mensaje por Telegram de forma asíncrona.
        
        Args:
            title: Título del mensaje
            message: Contenido del mensaje
        """
        full_text = f"📢 *{title}*\n\n{message}"
        
        async with self.telegram_bot:
            await self.telegram_bot.send_message(
                text=full_text,
                chat_id=self.chat_id,
                parse_mode='Markdown'
            )
