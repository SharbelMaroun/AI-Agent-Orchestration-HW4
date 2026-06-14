"""Docstring coverage for the public SDK API, DTOs, and exceptions (task 8.047)."""

import inspect

from archlens.sdk import dto_core, dto_loop
from archlens.sdk.sdk import ArchLensSDK
from archlens.shared import exceptions


def _public_classes(module):
    return [obj for name, obj in vars(module).items()
            if not name.startswith("_") and inspect.isclass(obj)
            and obj.__module__ == module.__name__]


def test_dtos_and_exceptions_have_docstrings():
    for module in (dto_core, dto_loop, exceptions):
        for cls in _public_classes(module):
            assert (cls.__doc__ or "").strip(), f"{module.__name__}.{cls.__name__}"


def test_sdk_public_methods_have_docstrings():
    for name in dir(ArchLensSDK):
        if name.startswith("_"):
            continue
        member = getattr(ArchLensSDK, name)
        if callable(member):
            assert (member.__doc__ or "").strip(), f"ArchLensSDK.{name}"
