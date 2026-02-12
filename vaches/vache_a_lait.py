from vaches.vache import Vache
from vaches.exceptions import InvalidVacheException
from vaches.strategies.protocoles.laitiere import RuminationLaitiere

class VacheALait(Vache):
    RENDEMENT_LAIT = 1.1
    PRODUCTION_LAIT_MAX = 40.0

    def __init__(self, petitNom: str, poids: float, panse: float = 0.0):
        super().__init__(petitNom, poids, panse)
        # On initialise la panse avec la valeur reçue (le parent la met à 0 par défaut)
        if panse < 0:
            raise InvalidVacheException("La panse initiale ne peut pas être négative.")
        if panse > self.PANSE_MAX:
            raise InvalidVacheException("La panse initiale dépasse la capacité maximale.")
        self._panse = float(panse)
        
        self._lait_disponible = 0.0
        self._lait_total_produit = 0.0
        self._lait_total_traite = 0.0
        
        self._strategy = RuminationLaitiere()

    @property
    def lait_disponible(self):
        return self._lait_disponible

    @property
    def lait_total_produit(self):
        return self._lait_total_produit

    @property
    def lait_total_traite(self):
        return self._lait_total_traite

    def traire(self, litres: float) -> float:
        if litres <= 0:
            raise InvalidVacheException("La quantité à traire doit être positive.")
        if litres > self._lait_disponible:
            raise InvalidVacheException("Quantité de lait insuffisante.")
        
        self._lait_disponible -= litres
        self._lait_total_traite += litres
        return litres

    # --- Hooks (Design Pattern Template Method) ---
    # _calculer_lait supprimé car délégué à la stratégie

    def _stocker_lait(self, quantite: float):
        self._lait_disponible += quantite
        self._lait_total_produit += quantite