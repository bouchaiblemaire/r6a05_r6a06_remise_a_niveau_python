from vaches.strategies.protocoles.rumination import RuminationStrategy
from vaches.exceptions import InvalidVacheException
from nourriture.TypeNourriture import TypeNourriture

class RuminationPieNoire(RuminationStrategy):
    """
    Stratégie PieNoire : produit du lait selon ration typée ou standard.
    """
    def calculer_production(self, vache, panse_avant: float) -> float:
        # Si pas de ration typée, comportement standard (VacheALait)
        if not vache._ration:
            # On pourrait réutiliser RuminationLaitiere, mais pour simplifier
            # on réimplémente ou on instancie RuminationLaitiere si besoin.
            # Ici, reprise de la logique VacheALait.
            rendement = getattr(vache, 'RENDEMENT_LAIT', 1.1)
            lait = rendement * panse_avant
            if vache.lait_disponible + lait > vache.PRODUCTION_LAIT_MAX:
                raise InvalidVacheException("La production de lait dépasse la capacité maximale de la vache.")
            return lait

        # Ration typée
        somme_ponderee = 0.0
        # On suppose que vache a COEFFICIENT_LAIT_PAR_NOURRITURE
        coef_map = getattr(vache, 'COEFFICIENT_LAIT_PAR_NOURRITURE', {})
        
        for type_n, quantite in vache._ration.items():
            coef = coef_map.get(type_n, 1.0)
            somme_ponderee += quantite * coef
        
        rendement_lait = getattr(vache, 'RENDEMENT_LAIT', 1.1)
        lait = rendement_lait * somme_ponderee
        
        if vache.lait_disponible + lait > vache.PRODUCTION_LAIT_MAX:
             raise InvalidVacheException("La production de lait dépasse la capacité maximale de la vache.")
        
        return lait

    def post_rumination(self, vache, panse_avant: float) -> None:
        if vache._ration:
            vache._ration.clear()
