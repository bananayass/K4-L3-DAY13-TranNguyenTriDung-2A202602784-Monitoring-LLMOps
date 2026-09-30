from app.pii import scrub_text


def test_scrub_email() -> None:
    out = scrub_text("Email me at student@vinuni.edu.vn")
    assert "student@" not in out
    assert "REDACTED_EMAIL" in out


def test_scrub_common_vietnamese_phone_formats() -> None:
    phone_numbers = (
        "0901234567",
        "090 123 4567",
        "090.123.4567",
        "090-123-4567",
        "+84 90 123 4567",
    )

    for phone_number in phone_numbers:
        out = scrub_text(f"Contact: {phone_number}")
        assert phone_number not in out
        assert "REDACTED_PHONE_VN" in out


def test_scrub_cccd() -> None:
    out = scrub_text("CCCD: 001203456789")
    assert "001203456789" not in out
    assert "REDACTED_CCCD" in out


def test_scrub_credit_card() -> None:
    out = scrub_text("Card: 4111-1111-1111-1111")
    assert "4111-1111-1111-1111" not in out
    assert "REDACTED_CREDIT_CARD" in out


def test_scrub_vietnamese_passport() -> None:
    out = scrub_text("Passport: C12345678")
    assert "C12345678" not in out
    assert "REDACTED_PASSPORT" in out


def test_scrub_labeled_vietnamese_address() -> None:
    address = "Địa chỉ: 123 Đường Lê Lợi, Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh"
    out = scrub_text(address)
    assert "123 Đường Lê Lợi" not in out
    assert "REDACTED_ADDRESS_VN" in out
