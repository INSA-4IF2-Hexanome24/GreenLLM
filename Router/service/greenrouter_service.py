"""Service for GreenKNNRouter utility scoring."""

import os
from typing import List, Dict, Any

from custom_routers.greenrouter import GreenKNNRouter


class UtilityScoringService:
    """Service pour scorer les requêtes avec le GreenKNNRouter."""

    _router_instance = None

    @classmethod
    def get_router(cls) -> GreenKNNRouter:
        """Charge ou récupère l'instance du GreenKNNRouter."""
        if cls._router_instance is None:
            project_root = os.path.dirname(os.path.dirname(__file__))
            config_path = os.path.join(
                project_root,
                "custom_routers/greenrouter/config.yaml",
            )
            if not os.path.exists(config_path):
                raise FileNotFoundError(
                    f"Configuration file not found: {config_path}"
                )
            cls._router_instance = GreenKNNRouter(yaml_path=config_path)
        return cls._router_instance

    @classmethod
    def score_query(cls, query_text: str) -> Dict[str, Any]:
        """
        Score une requête textuelle avec le GreenKNNRouter.

        Args:
            query_text: texte de la requête

        Returns:
            dict avec :
              - routers: liste des modèles avec leurs scores d'utilité, triés décroissant
              - difficulty_score: score de difficulté estimé [0,1]
              - threshold: seuil de difficulté du router
        """
        router = cls.get_router()

        # Routage de la requête
        result = router.route_single({"query": query_text})

        # Extraction et tri des scores d'utilité
        utility_scores = result.get("utility_scores", {})
        routers = [
            {
                "model": model,
                "utility": float(score),
                "performance": float(result.get("perf_scores", {}).get(model, 0.0)),
                "co2": float(result.get("co2_scores", {}).get(model, 0.0)),
            }
            for model, score in utility_scores.items()
        ]

        # Tri par utilité décroissante
        routers.sort(key=lambda x: x["utility"], reverse=True)
        model_name = result.get("model_name")
        if( model_name == "web_search" ):
            return{
                        "routers": routers,
                        "difficulty_score": float(result.get("difficulty_score", 0.0)),
                        "threshold": float(result.get("threshold", 0.0)),
                        "best_model": model_name,
                        "answers": result.get("answers", []),
                }
        else:
            return {
                "routers": routers,
                "difficulty_score": float(result.get("difficulty_score", 0.0)),
                "threshold": float(result.get("threshold", 0.0)),
                "best_model": model_name,
            }
