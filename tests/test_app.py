import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import app


def test_app_exists():
    assert app.app is not None


def test_layout_exists():
    assert app.app.layout is not None


def test_header_text():
    layout_str = str(app.app.layout)
    assert "Pink Morsel Sales Visualiser" in layout_str


def test_radio_items_present():
    layout_str = str(app.app.layout)
    for label in ["All", "North", "South", "East", "West"]:
        assert label in layout_str
