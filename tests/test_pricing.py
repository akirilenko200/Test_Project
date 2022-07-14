import pytest
from pricing import Pricing

# I. Negative scenarios:
# Testing inputs to the calculate
def test_number_of_items_raises_if_not_int():
    disc = {'1000': 3, '5000': 5, '7000': 7, '10000': 10}
    tax = {'AB': 5, 'ON': 13, 'QC': 14.975, 'MI': 6, 'DE': 0}
    p = Pricing(discounts=disc,tax_rates=tax)
    with pytest.raises(TypeError):
        p.calculate('asd', 10.0, 'AB')
    with pytest.raises(TypeError):
        p.calculate(3.4, 10.0, 'AB')

def test_number_of_items_raises_if_not_positive():
    disc = {'1000': 3, '5000': 5, '7000': 7, '10000': 10}
    tax = {'AB': 5, 'ON': 13, 'QC': 14.975, 'MI': 6, 'DE': 0}
    p = Pricing(discounts=disc,tax_rates=tax)
    with pytest.raises(ValueError):
        p.calculate(-5, 10.0, 'AB')

def test_price_per_item_raises_if_not_numeric():
    disc = {'1000': 3, '5000': 5, '7000': 7, '10000': 10}
    tax = {'AB': 5, 'ON': 13, 'QC': 14.975, 'MI': 6, 'DE': 0}
    p = Pricing(discounts=disc,tax_rates=tax)
    with pytest.raises(TypeError):
        p.calculate(1, '10.0', 'AB')

def test_price_per_item_raises_if_not_positive():
    disc = {'1000': 3, '5000': 5, '7000': 7, '10000': 10}
    tax = {'AB': 5, 'ON': 13, 'QC': 14.975, 'MI': 6, 'DE': 0}
    p = Pricing(discounts=disc,tax_rates=tax)
    with pytest.raises(ValueError):
        p.calculate(12, -10.0, 'AB')

def test_region_code_raises_if_not_valid():
    disc = {'1000': 3, '5000': 5, '7000': 7, '10000': 10}
    tax = {'AB': 5, 'ON': 13, 'QC': 14.975, 'MI': 6, 'DE': 0}
    p = Pricing(discounts=disc,tax_rates=tax)
    with pytest.raises(ValueError):
        p.calculate(12, 10.0, 'HELLO')

# II. Positive scenarios:

def test_positive_path():
    disc = {'1000': 3, '5000': 5, '7000': 7, '10000': 10}
    tax = {'AB': 5, 'ON': 13, 'QC': 14.975, 'MI': 6, 'DE': 0}
    p = Pricing(discounts=disc,tax_rates=tax)
    amount1 = p.calculate(13, 13264.7, 'ON')
    pytest.approx(amount1, 13*13264.7*0.9*1.13, 1e-5)

def test_different_discounts():
    disc = {'1000': 3, '5000': 5, '7000': 7, '10000': 10}
    tax = {'AB': 5, 'ON': 13, 'QC': 14.975, 'MI': 6, 'DE': 0}
    p = Pricing(discounts=disc,tax_rates=tax)
    # tax is assumed to be zero: DE
    amount1 = p.calculate(1, 10, 'DE')
    pytest.approx(amount1, 1*10, 1e-5)
    
    amount2 = p.calculate(1, 1001, 'DE')
    pytest.approx(amount2, 1*1001*(100 - 3) / 100, 1e-5)

    amount3 = p.calculate(1, 5001, 'DE')
    pytest.approx(amount3, 1*5001*(100 - 5) / 100, 1e-5)

    amount4 = p.calculate(1, 7001, 'DE')
    pytest.approx(amount4, 1*7001*(100 - 5) / 100, 1e-5)

    amount5 = p.calculate(1, 10001, 'DE')
    pytest.approx(amount5, 1*10001*(100 - 5) / 100, 1e-5)


def test_different_taxes():
    disc = {'1000': 3, '5000': 5, '7000': 7, '10000': 10}
    tax = {'AB': 5, 'ON': 13, 'QC': 14.975, 'MI': 6, 'DE': 0}
    p = Pricing(discounts=disc,tax_rates=tax)
    # discount is assumed to be zero
    amount1 = p.calculate(1, 10, 'AB')
    pytest.approx(amount1, 1*10*(100 + 5) / 100, 1e-5)
    
    amount2 = p.calculate(1, 10, 'ON')
    pytest.approx(amount2, 1*10*(100 + 13) / 100, 1e-5)

    amount3 = p.calculate(1, 10, 'QC')
    pytest.approx(amount3, 1*10*(100 + 14.975) / 100, 1e-5)

    amount4 = p.calculate(1, 10, 'MI')
    pytest.approx(amount4, 1*10*(100 + 6) / 100, 1e-5)

    amount5 = p.calculate(1, 10, 'DE')
    pytest.approx(amount5, 1*10*(100 - 0) / 100, 1e-5)


def test_discounts_empty():
    disc = {}
    tax = {'AB': 5, 'ON': 13, 'QC': 14.975, 'MI': 6, 'DE': 0}
    p = Pricing(discounts=disc,tax_rates=tax)
    amount1 = p.calculate(10, 10000, 'AB')
    pytest.approx(amount1, 10*10000*(100 + 5) / 100, 1e-5)


def test_discounts_single():
    disc = {'10000': 10}
    tax = {'AB': 5, 'ON': 13, 'QC': 14.975, 'MI': 6, 'DE': 0}
    p = Pricing(discounts=disc,tax_rates=tax)
    # above
    amount1 = p.calculate(10, 10000, 'AB')
    pytest.approx(amount1, 10*10000*0.9*(100 + 5) / 100, 1e-5)
    # below
    amount2 = p.calculate(10, 10, 'AB')
    pytest.approx(amount2, 10*10*(100 + 5) / 100, 1e-5)

def test_discounts_when_unsorted():
    disc = {'5000': 5, '10000': 10,  '1000': 3,  '7000': 7}
    tax = {'AB': 5, 'ON': 13, 'QC': 14.975, 'MI': 6, 'DE': 0}
    p = Pricing(discounts=disc,tax_rates=tax)

    amount1 = p.calculate(1, 10, 'DE')
    pytest.approx(amount1, 1*10, 1e-5)
    
    amount2 = p.calculate(1, 1001, 'DE')
    pytest.approx(amount2, 1*1001*(100 - 3) / 100, 1e-5)

    amount3 = p.calculate(1, 5001, 'DE')
    pytest.approx(amount3, 1*5001*(100 - 5) / 100, 1e-5)

    amount4 = p.calculate(1, 7001, 'DE')
    pytest.approx(amount4, 1*7001*(100 - 5) / 100, 1e-5)

    amount5 = p.calculate(1, 10001, 'DE')
    pytest.approx(amount5, 1*10001*(100 - 5) / 100, 1e-5)

