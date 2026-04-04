class UncertaintyEngine:

    @staticmethod
    def cecph7(p10, p50, p90):
        return {
            "mean": float(p50),
            "lower": float(p10),
            "upper": float(p90),
            "width": float(p90 - p10),
        }

    @staticmethod
    def bdfiod(mu, sigma):
        lower = mu - 1.28 * sigma
        upper = mu + 1.28 * sigma

        return {
            "mean": float(mu),
            "lower": float(lower),
            "upper": float(upper),
            "width": float(upper - lower),
            "sigma": float(sigma),
        }

    @staticmethod
    def totc(q05, q50, q95):
        return {
            "mean": float(q50),
            "lower": float(q05),
            "upper": float(q95),
            "width": float(q95 - q05),
        }