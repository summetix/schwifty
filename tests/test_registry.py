from schwifty import BIC
from schwifty import registry


def test_validate_bics():
    for bic in (bank["bic"] for bank in registry.get("bank") if bank["bic"]):
        BIC(bic, allow_invalid=False)


def test_validate_cz_encoding():
    assert "Komerční banka, a.s.", "Československá obchodní banka, a. s." in [
        bank["name"] for bank in registry.get("bank") if bank["country_code"] == "CZ"
    ]
