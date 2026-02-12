from vaches.vache_a_lait import VacheALait
from vaches.exceptions import InvalidVacheException
from nourriture.TypeNourriture import TypeNourriture
from vaches.strategies.pie_noire import RuminationPieNoire

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
        # Surcharge de la stratégie
        self._strategy = RuminationPieNoire()

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
        # self.brouter() dans Vache ferait un check "nourriture is not None" qui failerait.
        # Donc on contourne en appelant le brouter de Vache SANS nourriture, 
        # car on a déjà géré la partie "nourriture" ci-dessus.
        
        # Astuce : on appelle Vache.brouter(self, quantite) directement pour éviter la surcharge éventuelle
        # ou simplement super().brouter(quantite) car VacheALait n'a pas de brouter.
        
        # IMPORTANT: Vache.brouter(quantite, nourriture=None) lève une exception si nourriture n'est pas None.
        # Ici on appelle super().brouter(quantite) (donc nourriture=None implicite), ce qui est valide pour Vache.
        super(VacheALait, self).brouter(quantite)

    # Les hooks _calculer_lait et _post_rumination sont supprimés car gérés par la stratégie.
