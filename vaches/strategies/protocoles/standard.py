from vaches.strategies.protocoles.rumination import RuminationStrategy

class RuminationStandard(RuminationStrategy):
    """
    Stratégie standard : une vache normale ne produit pas de lait.
    """
    def calculer_production(self, vache, panse_avant: float) -> float:
        return 0.0

    def post_rumination(self, vache, panse_avant: float) -> None:
        pass
