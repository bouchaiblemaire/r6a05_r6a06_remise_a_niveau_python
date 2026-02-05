from vaches.vache_a_lait import VacheALait
from vaches.exceptions import InvalidVacheException
from nourriture.TypeNourriture import TypeNourriture

class PieNoire(VacheALait):
    # --- Constantes ---
    COEFFICIENT_LAIT_PAR_NOURRITURE: dict[TypeNourriture, float] = {
        TypeNourriture.MARGUERITE: 1.1,
        TypeNourriture.HERBE: 1.0,
        TypeNourriture.FOIN: 0.9,
        TypeNourriture.PAILLE: 0.4,
        TypeNourriture.CEREALES: 1.3,
    }

    def __init__(self, petitNom: str, poids: float, age: int, panse: float = 0.0):
        super().__init__(petitNom, poids, age, panse)
        self._ration: dict[TypeNourriture, float] = {}

    def brouter(self, quantite: float, nourriture: TypeNourriture = None):
        if quantite <= 0:
            raise InvalidVacheException("La quantité broutée doit être positive.")
        
        if self._panse + quantite > self.PANSE_MAX:
             raise InvalidVacheException("Capacité de la panse dépassée.")

        if nourriture is not None:
            if not isinstance(nourriture, TypeNourriture):
                raise InvalidVacheException("Type de nourriture invalide.")
            
            # Initialiser le type s'il n'existe pas dans la ration
            if nourriture not in self._ration:
                self._ration[nourriture] = 0.0
            self._ration[nourriture] += quantite
        
        # On met à jour la panse via la logique de base (Vache)
        # Mais VacheALait n'overload pas brouter, Vache le fait.
        # Dans Vache.brouter(quantite, nourriture=None):
        # if nourriture is not None: raise InvalidVacheException
        
        # So we should call Vache.brouter(quantite) directly or avoid calling super().brouter(quantite, nourriture)
        # if we want to bypass the "no food" check.
        # However, Vache.brouter performs the panse limit check.
        
        # Let's bypass the "no food" check by calling the implementation logic or 
        # by calling super(VacheALait, self).brouter(quantite) if we want to target Vache.
        # Actually Vache is the one that has the check.
        
        # If I call super().brouter(quantite), it calls VacheALait.brouter (not defined) -> Vache.brouter.
        # But Vache.brouter(quantite) is fine, it only raises if nourriture is NOT None.
        
        super(VacheALait, self).brouter(quantite) # This calls Vache.brouter(quantite)

    def _calculer_lait(self, panse_avant: float) -> float:
        if not self._ration:
            return super()._calculer_lait(panse_avant)
        
        # Calcul basé sur la ration typée
        somme_ponderee = 0.0
        for type_n, quantite in self._ration.items():
            coef = self.COEFFICIENT_LAIT_PAR_NOURRITURE.get(type_n, 1.0)
            somme_ponderee += quantite * coef
        
        lait = self.RENDEMENT_LAIT * somme_ponderee
        
        if self._lait_disponible + lait > self.PRODUCTION_LAIT_MAX:
             raise InvalidVacheException("La production de lait dépasse la capacité maximale de la vache.")
        
        return lait

    def _post_rumination(self, panse_avant: float):
        # La ration typée est consommée après rumination
        self._ration.clear()
