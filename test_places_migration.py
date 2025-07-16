#!/usr/bin/env python3
"""
Test script for Google Places API migration
Run this to test both legacy and new API functionality
"""

import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure Django settings
if not settings.configured:
    settings.configure(
        DEBUG=True,
        INSTALLED_APPS=[
            "django.contrib.gis",
            "mapwidgets",
        ],
        MAP_WIDGETS={
            "GoogleMap": {
                "apiKey": os.environ.get("GOOGLE_MAP_API_KEY", "test-key"),
                "PointField": {
                    "interactive": {
                        "useNewPlacesAPI": "auto",
                        "autoFallbackToLegacy": True,
                        "GooglePlaceAutocompleteOptions": {
                            "componentRestrictions": {"country": "us"},
                            "types": ["address"],
                        },
                    }
                },
            }
        },
        USE_TZ=True,
    )

django.setup()

import json

from mapwidgets.settings import mw_settings
from mapwidgets.widgets import GoogleMapPointFieldWidget


def test_settings_migration():
    """Test that new settings are properly loaded"""
    print("Testing settings migration...")

    # Check that new settings are available
    interactive_settings = mw_settings.GoogleMap.PointField.interactive

    assert hasattr(
        interactive_settings, "useNewPlacesAPI"
    ), "useNewPlacesAPI setting missing"
    assert hasattr(
        interactive_settings, "autoFallbackToLegacy"
    ), "autoFallbackToLegacy setting missing"

    print(f"✓ useNewPlacesAPI: {interactive_settings.useNewPlacesAPI}")
    print(f"✓ autoFallbackToLegacy: {interactive_settings.autoFallbackToLegacy}")


def test_widget_initialization():
    """Test that widget initializes with new settings"""
    print("\nTesting widget initialization...")

    widget = GoogleMapPointFieldWidget()

    # Check that widget has access to settings
    settings_dict = widget.settings
    assert "useNewPlacesAPI" in settings_dict, "useNewPlacesAPI not in widget settings"
    assert (
        "autoFallbackToLegacy" in settings_dict
    ), "autoFallbackToLegacy not in widget settings"

    print(f"✓ Widget settings include migration options")


def test_context_generation():
    """Test that widget context includes new options"""
    print("\nTesting context generation...")

    widget = GoogleMapPointFieldWidget()
    context = widget.get_context("test_field", None, {})

    # Parse the options JSON
    options = json.loads(context["options"])

    assert "useNewPlacesAPI" in options, "useNewPlacesAPI not in context"
    assert "autoFallbackToLegacy" in options, "autoFallbackToLegacy not in context"

    print(f"✓ Context includes useNewPlacesAPI: {options['useNewPlacesAPI']}")
    print(f"✓ Context includes autoFallbackToLegacy: {options['autoFallbackToLegacy']}")


def test_different_configurations():
    """Test different API configuration scenarios"""
    print("\nTesting different configurations...")

    test_configs = [
        {"useNewPlacesAPI": "auto", "expected": "auto"},
        {"useNewPlacesAPI": "new", "expected": "new"},
        {"useNewPlacesAPI": "legacy", "expected": "legacy"},
    ]

    for config in test_configs:
        # Temporarily override settings
        original_settings = dict(mw_settings.GoogleMap.PointField.interactive)
        mw_settings.GoogleMap.PointField.interactive.update(config)

        widget = GoogleMapPointFieldWidget()
        context = widget.get_context("test_field", None, {})
        options = json.loads(context["options"])

        assert (
            options["useNewPlacesAPI"] == config["expected"]
        ), f"Expected {config['expected']}, got {options['useNewPlacesAPI']}"
        print(f"✓ Configuration {config['useNewPlacesAPI']} works correctly")

        # Restore original settings
        mw_settings.GoogleMap.PointField.interactive.clear()
        mw_settings.GoogleMap.PointField.interactive.update(original_settings)


def main():
    """Run all tests"""
    print("Google Places API Migration Test Suite")
    print("=" * 50)

    try:
        test_settings_migration()
        test_widget_initialization()
        test_context_generation()
        test_different_configurations()

        print("\n" + "=" * 50)
        print("✅ All tests passed! Migration is ready.")
        print("\nNext steps:")
        print("1. Set GOOGLE_MAP_API_KEY environment variable")
        print("2. Test in a real Django application")
        print("3. Verify both legacy and new API work in browser")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
