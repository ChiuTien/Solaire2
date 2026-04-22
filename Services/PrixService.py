class PrixService:
    @staticmethod
    def prix_achat(consommation_restante, energie_unitaire, prix_ouvrable, prix_weekend):
        if prix_ouvrable == 0 or prix_weekend == 0:
            raise ValueError("prix_ouvrable et prix_weekend doivent etre differents de 0")

        if energie_unitaire == 0:
            raise ValueError("energie_unitaire doit etre different de 0")

        ouvrable = (float(consommation_restante) * float(prix_ouvrable) / float(energie_unitaire)) * 5
        weekend = (float(consommation_restante) * float(prix_weekend) / float(energie_unitaire)) * 2

        return [ouvrable, weekend]

    @staticmethod
    def prix_achat_depuis_config(consommation_restante, energie_unitaire, prix_config):
        return PrixService.prix_achat(
            consommation_restante=consommation_restante,
            energie_unitaire=energie_unitaire,
            prix_ouvrable=prix_config.get_prixOuvrable(),
            prix_weekend=prix_config.get_prixWeekend(),
        )
