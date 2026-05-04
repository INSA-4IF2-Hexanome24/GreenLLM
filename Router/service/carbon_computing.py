"""Carbon footprint computation helpers for the FastAPI endpoint."""

CARBON_COST_PER_TOKEN = {
	"gpt-4": 0.00000015,
	"gpt-4-turbo": 0.00000012,
	"gpt-3.5-turbo": 0.00000005,
	"claude-3-opus": 0.00000018,
	"claude-3-sonnet": 0.00000008,
	"llama-2-70b": 0.00000004,
	"mistral-7b": 0.00000002,
	"gemini-pro": 0.00000010,
}

ESTIMATED_OUTPUT_TOKENS = {
	"gpt-4": 150,
	"gpt-4-turbo": 140,
	"gpt-3.5-turbo": 120,
	"claude-3-opus": 160,
	"claude-3-sonnet": 130,
	"llama-2-70b": 110,
	"mistral-7b": 100,
	"gemini-pro": 125,
}


def calculate_request_carbon_footprint() -> dict:
	"""Return mock carbon footprint metrics for each model.

	The request input size is fixed for now, while output tokens depend on the model.
	"""
	input_tokens = 50

	results = {
		"request_metrics": {
			"input_tokens": input_tokens,
		},
		"models": {},
	}

	for model, carbon_per_token in CARBON_COST_PER_TOKEN.items():
		output_tokens = ESTIMATED_OUTPUT_TOKENS.get(model, 100)
		total_tokens = input_tokens + output_tokens
		total_carbon = carbon_per_token * total_tokens

		results["models"][model] = {
			"output_tokens_estimated": output_tokens,
			"total_tokens": total_tokens,
			"carbon_cost_per_token_kg_co2": carbon_per_token,
			"total_carbon_cost_kg_co2": round(total_carbon, 10),
			"total_carbon_cost_mg_co2": round(total_carbon * 1_000_000, 3),
		}

	sorted_models = sorted(
		results["models"].items(),
		key=lambda item: item[1]["total_carbon_cost_kg_co2"],
	)

	results["models_sorted_by_greenest"] = [
		{"model": model, **metrics} for model, metrics in sorted_models
	]

	return results
