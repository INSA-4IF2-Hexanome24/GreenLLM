from llmrouter.models.knnrouter.router import KNNRouter

config_path = "configs/model_config_train/knnrouter.yaml"
router = KNNRouter(config_path)

result = router.route_single({"query": "What is machine learning?"})
print("Résultat du routing :", result)