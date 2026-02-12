from typing import Protocol

class RuminationStrategy(Protocol):
    def calculer_production(self, vache, panse_avant: float) -> float:
        """
        Calcule la quantité de lait produite lors de la rumination.
        :param vache: L'instance de la vache (pour accéder à ses attributs si nécessaire)
        :param panse_avant: La quantité dans la panse avant rumination
        :return: La quantité de lait produite
        """
        ...

    def post_rumination(self, vache, panse_avant: float) -> None:
        """
        Effectue des actions après la rumination (ex: vider la ration typée).
        :param vache: L'instance de la vache
        :param panse_avant: La quantité dans la panse avant rumination
        """
        ...