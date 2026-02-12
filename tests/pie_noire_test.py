import pytest
from vaches.pie_noire import PieNoire
from vaches.exceptions import InvalidVacheException
from nourriture.TypeNourriture import TypeNourriture

def test_pie_noire_init():
    vache = PieNoire("Bella", 600.0)
    assert vache.petitNom == "Bella"
    assert vache._poids == 600.0
    assert vache._age == 0
    assert vache.panse == 0.0
    assert vache._ration == {}

def test_pie_noire_brouter_no_type():
    vache = PieNoire("Bella", 600.0)
    vache.brouter(10.0)
    assert vache.panse == 10.0
    assert vache._ration == {}

def test_pie_noire_brouter_with_type():
    vache = PieNoire("Bella", 600.0)
    vache.brouter(5.0, TypeNourriture.HERBE)
    vache.brouter(3.0, TypeNourriture.FOIN)
    assert vache.panse == 8.0
    assert vache._ration[TypeNourriture.HERBE] == 5.0
    assert vache._ration[TypeNourriture.FOIN] == 3.0

def test_pie_noire_ruminer_with_typed_ration():
    vache = PieNoire("Bella", 600.0)
    # 10kg HERBE (coef 1.0) -> production: 1.1 * (10 * 1.0) = 11.0
    vache.brouter(10.0, TypeNourriture.HERBE)
    
    poids_avant = vache.poids
    lait_produit = vache.ruminer()
    
    assert lait_produit == pytest.approx(11.0)
    assert vache.lait_disponible == pytest.approx(11.0)
    assert vache.panse == 0.0
    assert vache._ration == {}
    # Gain poids: 0.25 * 10 = 2.5
    assert vache.poids == pytest.approx(poids_avant + 2.5)

def test_pie_noire_ruminer_with_mixed_typed_ration():
    vache = PieNoire("Bella", 600.0)
    # 5kg CEREALES (coef 1.3), 5kg PAILLE (coef 0.4)
    # production: 1.1 * (5 * 1.3 + 5 * 0.4) = 1.1 * (6.5 + 2.0) = 1.1 * 8.5 = 9.35
    vache.brouter(5.0, TypeNourriture.CEREALES)
    vache.brouter(5.0, TypeNourriture.PAILLE)
    
    lait_produit = vache.ruminer()
    
    assert lait_produit == pytest.approx(9.35)
    assert vache.lait_disponible == pytest.approx(9.35)
    assert vache._ration == {}

def test_pie_noire_ruminer_no_typed_ration_fallback():
    vache = PieNoire("Bella", 600.0)
    # 10kg sans type -> production standard: 1.1 * 10 = 11.0
    vache.brouter(10.0)
    
    lait_produit = vache.ruminer()
    
    assert lait_produit == pytest.approx(11.0)
    assert vache.lait_disponible == pytest.approx(11.0)

def test_pie_noire_brouter_exceed_panse():
    vache = PieNoire("Bella", 600.0)
    with pytest.raises(InvalidVacheException, match="Capacité de la panse dépassée"):
        vache.brouter(vache.PANSE_MAX + 1)

def test_pie_noire_ruminer_exceed_lait_max():
    vache = PieNoire("Bella", 600.0)
    # PRODUCTION_LAIT_MAX = 40.0
    # Avec CEREALES (coef 1.3), 1.1 * (Q * 1.3) > 40.0 -> Q > 40 / (1.1 * 1.3) = 40 / 1.43 ≈ 27.97
    vache.brouter(30.0, TypeNourriture.CEREALES)
    
    with pytest.raises(InvalidVacheException, match="La production de lait dépasse la capacité maximale"):
        vache.ruminer()

def test_pie_noire_brouter_invalid_type():
    vache = PieNoire("Bella", 600.0)
    with pytest.raises(InvalidVacheException, match="Type de nourriture invalide"):
        vache.brouter(5.0, "NOT_AN_ENUM")