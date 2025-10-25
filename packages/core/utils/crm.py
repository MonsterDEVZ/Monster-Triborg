"""
Модуль для интеграции с AmoCRM через вебхуки
"""
import asyncio
import logging
import aiohttp
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


async def send_to_crm(
    webhook_url: str, payload: Dict[str, Any], timeout: int = 10
) -> bool:
    """
    Универсальная функция для отправки данных в AmoCRM через вебхук

    Args:
        webhook_url: URL вебхука AmoCRM
        payload: Словарь с данными для отправки
        timeout: Таймаут запроса в секундах (по умолчанию 10)

    Returns:
        bool: True если отправка успешна, False в случае ошибки

    Example:
        >>> payload = {
        ...     "lead_name": "Новый лид с Telegram: MONSTER AGENCY",
        ...     "contact": {
        ...         "name": "John Doe",
        ...         "username": "@johndoe"
        ...     },
        ...     "source": "Telegram Bot",
        ...     "request_details": "Привлечь клиентов"
        ... }
        >>> success = await send_to_crm(webhook_url, payload)
    """
    try:
        logger.info(f"📤 Отправка лида в AmoCRM: {webhook_url}")
        logger.debug(f"📋 Payload: {payload}")

        async with aiohttp.ClientSession() as session:
            async with session.post(
                webhook_url,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=timeout),
                headers={"Content-Type": "application/json"},
            ) as response:
                # Проверяем статус ответа
                if response.status in (200, 201, 202):
                    response_text = await response.text()
                    logger.info(
                        f"✅ Лид успешно отправлен в AmoCRM. Статус: {response.status}"
                    )
                    logger.debug(f"📥 Ответ: {response_text}")
                    return True
                else:
                    error_text = await response.text()
                    logger.error(
                        f"❌ Ошибка отправки в AmoCRM. "
                        f"Статус: {response.status}, Ответ: {error_text}"
                    )
                    return False

    except aiohttp.ClientConnectorError as e:
        # CRM-сервер недоступен (не удалось установить соединение)
        logger.error(
            f"❌ CRM-сервер недоступен (ошибка соединения): {e}",
            exc_info=True
        )
        return False

    except aiohttp.ClientResponseError as e:
        # CRM ответила с ошибкой (4xx, 5xx)
        logger.error(
            f"❌ CRM вернула ошибку. Статус: {e.status}, Сообщение: {e.message}",
            exc_info=True
        )
        return False

    except asyncio.TimeoutError:
        # Таймаут запроса
        logger.error(f"❌ Таймаут при отправке в AmoCRM (>{timeout}s)")
        return False

    except aiohttp.ClientError as e:
        # Другие ошибки aiohttp
        logger.error(
            f"❌ Ошибка HTTP-клиента при отправке в AmoCRM: {e}",
            exc_info=True
        )
        return False

    except Exception as e:
        # Неожиданные ошибки
        logger.error(
            f"❌ Неожиданная ошибка при отправке в AmoCRM: {e}",
            exc_info=True
        )
        return False


def build_crm_payload(
    brand_name: str,
    contact_name: str,
    username: str,
    request_details: str,
    phone: Optional[str] = None,
    additional_data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Формирование стандартизированного payload для AmoCRM

    Args:
        brand_name: Название бренда (MONSTER AGENCY, MONSTER CG, MONSTER EXPRESS)
        contact_name: Имя контакта из Telegram
        username: Username пользователя (с @)
        request_details: Детали запроса (выбранная опция)
        phone: Номер телефона пользователя (опционально)
        additional_data: Дополнительные данные (опционально)

    Returns:
        Dict[str, Any]: Стандартизированный payload для AmoCRM
    """
    # Формируем контактные данные
    contact_data = {"name": contact_name, "username": username}

    # Добавляем телефон, если предоставлен
    if phone:
        contact_data["phone"] = phone

    payload = {
        "lead_name": f"Новый лид с Telegram: {brand_name}",
        "contact": contact_data,
        "source": "Telegram Bot",
        "request_details": request_details,
    }

    # Добавляем дополнительные данные, если есть
    if additional_data:
        payload.update(additional_data)

    return payload
