"""Simple plugin registry for replaceable components."""

from collections import defaultdict
from typing import Any, Callable

from core.exceptions import PluginNotFoundError

_REGISTRY: dict[str, dict[str, type]] = defaultdict(dict)


def register_plugin(category: str, name: str) -> Callable[[type], type]:
    """Decorator for registering a plugin class in a category."""

    def decorator(cls: type) -> type:
        _REGISTRY[category][name] = cls
        return cls

    return decorator


def create_plugin(category: str, name: str, **kwargs: Any) -> Any:
    """Create an instance of a registered plugin."""
    plugins = _REGISTRY.get(category, {})
    if name not in plugins:
        raise PluginNotFoundError(f"Plugin '{name}' not found in category '{category}'.")
    return plugins[name](**kwargs)


def list_plugins(category: str) -> list[str]:
    """List plugin names in a category."""
    return sorted(_REGISTRY.get(category, {}).keys())


def list_all_plugins() -> dict[str, list[str]]:
    """List all registered plugins grouped by category."""
    return {category: sorted(plugins.keys()) for category, plugins in sorted(_REGISTRY.items())}


