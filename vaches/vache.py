from vaches.exceptions import InvalidVacheException

from vaches.strategies.protocoles.rumination import RuminationStrategy
from vaches.strategies.standard import RuminationStandard

class Vache:
    # --- Constantes ---
    AGE_MAX = 25
    POIDS_MAX = 1000.0
    PANSE_MAX = 200.0
    RENDEMENT_RUMINATION = 0.25

    def __init__(self, petitNom: str, poids: float, age: int, panse: float = 0.0):
        # Validation du nom (non vide, pas que des espaces)
        if not petitNom or not petitNom.strip():
            raise InvalidVacheException("Le petit nom ne peut pas être vide.")
        
        # Validation de l'âge
        if not (0 <= age <= self.AGE_MAX):
            raise InvalidVacheException(f"L'âge doit être entre 0 et {self.AGE_MAX} ans.")
        
        # Validation du poids
        if poids < 0 or poids > self.POIDS_MAX:
            raise InvalidVacheException("Le poids doit être entre 0 et 1000kg.")
            
        self.petitNom = petitNom
        self._poids = poids
        self._age = age
        self._panse = panse
        self._lait_disponible = 0.0
        self._lait_total_produit = 0.0
        self._lait_total_traite = 0.0
        
        # Initialisation de la stratégie par défaut
        self._strategy: RuminationStrategy = RuminationStandard()

    # --- Properties (pour accès contrôlé) ---
    @property
    def poids(self):
        return self._poids

    @property
    def age(self):
        return self._age

    @property
    def panse(self):
        return self._panse

    # --- Méthodes Métier ---
    def brouter(self, quantite: float, nourriture=None):
        if quantite <= 0:
            raise InvalidVacheException("La quantité broutée doit être positive.")
        
        if nourriture is not None:
             raise InvalidVacheException("Une vache standard ne peut pas brouter de nourriture typée.")

        if self._panse + quantite > self.PANSE_MAX:
             raise InvalidVacheException("Capacité de la panse dépassée.")
        
        self._panse += quantite

    def vieillir(self):
        if self._age + 1 > self.AGE_MAX:
            raise InvalidVacheException("La vache a atteint son âge maximum.")
        self._age += 1

    def ruminer(self) -> float:
        """
        Template Method : définit le squelette de l'algorithme de rumination.
        Utilise maintenant une Stratégie pour les calculs.
        """
        # 1. Vérification
        if self._panse <= 0:
            raise InvalidVacheException("La panse est vide, impossible de ruminer.")

        # 2. Mémorisation
        panse_avant = self._panse

        # 3. Gain de poids
        gain_poids = self.RENDEMENT_RUMINATION * panse_avant
        self._poids += gain_poids

        # 4. Calcul production de lait (via Stratégie)
        lait_produit = self._strategy.calculer_production(self, panse_avant)

        # 5. Stockage du lait (Hook conservé ou géré par VacheALait)
        self._stocker_lait(lait_produit)

        # 6. Vider la panse
        self._panse = 0.0

        # 7. Post-traitement (via Stratégie)
        self._strategy.post_rumination(self, panse_avant)

        # 8. Retourner la quantité
        return lait_produit

    # --- Hooks ---
    def _stocker_lait(self, quantite: float):
        pass


