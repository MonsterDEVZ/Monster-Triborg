"""
Утилиты для работы с локализацией
"""
import json
from typing import Dict, Any, Optional
from packages.core.utils.config import config


class LocaleManager:
    """Менеджер локализации для загрузки текстов из locales.json"""

    def __init__(self):
        self._locales: Dict[str, Any] = {}
        self.load_locales()

    def load_locales(self):
        """Загрузка локализации из JSON файла"""
        try:
            with open(config.LOCALES_PATH, "r", encoding="utf-8") as f:
                self._locales = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Файл локализации не найден: {config.LOCALES_PATH}"
            )
        except json.JSONDecodeError as e:
            raise ValueError(f"Ошибка парсинга locales.json: {e}")

    def get_fallback(self) -> Dict[str, Any]:
        """Получить данные для fallback сценария"""
        return self._locales.get("fallback", {})

    def get_profile(self, profile_name: str) -> Optional[Dict[str, Any]]:
        """
        Получить данные профиля по названию (agency, cg, express)

        Args:
            profile_name: Название профиля (agency, cg, express)

        Returns:
            Словарь с данными профиля или None
        """
        return self._locales.get(profile_name)

    def get_step1_data(self, profile_name: str) -> Dict[str, Any]:
        """Получить данные для Шага 1"""
        profile = self.get_profile(profile_name)
        if not profile:
            raise ValueError(f"Профиль {profile_name} не найден")
        return profile.get("step1", {})

    def get_step2_data(self, profile_name: str) -> Dict[str, Any]:
        """Получить данные для Шага 2"""
        profile = self.get_profile(profile_name)
        if not profile:
            raise ValueError(f"Профиль {profile_name} не найден")
        return profile.get("step2", {})

    def get_followup_data(self, profile_name: str) -> Dict[str, Any]:
        """Получить данные для follow-up сообщений"""
        profile = self.get_profile(profile_name)
        if not profile:
            raise ValueError(f"Профиль {profile_name} не найден")
        return profile.get("followup", {})

    def get_choice_text(self, profile_name: str, callback_data: str) -> str:
        """
        Получить текст выбранной опции по callback_data

        Args:
            profile_name: Название профиля
            callback_data: callback_data кнопки

        Returns:
            Текст выбора
        """
        step2 = self.get_step2_data(profile_name)
        choices = step2.get("choices", {})
        return choices.get(callback_data, callback_data)


# Глобальный экземпляр менеджера локализации
locale_manager = LocaleManager()
