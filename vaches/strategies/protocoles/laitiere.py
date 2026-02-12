from vaches.strategies.protocoles.rumination import RuminationStrategy
from vaches.exceptions import InvalidVacheException

class RuminationLaitiere(RuminationStrategy):
    """
    Stratégie laitière : produit du lait en fonction du rendement de la vache.
    """
    def calculer_production(self, vache, panse_avant: float) -> float:
        # VacheALait.RENDEMENT_LAIT est une constante de classe sur VacheALait
        # Mais ici 'vache' est une instance. Si RuminationLaitiere est utilisée par VacheALait,
        # on peut accéder à vache.RENDEMENT_LAIT ou self.VacheClass.RENDEMENT_LAIT
        
        # Le plus propre est d'utiliser les attributs/constantes de l'instance 'vache'
        rendement = getattr(vache, 'RENDEMENT_LAIT', 1.1) 
        lait = rendement * panse_avant
        
        # Vérification capacité
        if vache.lait_disponible + lait > vache.PRODUCTION_LAIT_MAX:
             raise InvalidVacheException("La production de lait dépasse la capacité maximale de la vache.")
        
        return lait

    def post_rumination(self, vache, panse_avant: float) -> None:
        pass
