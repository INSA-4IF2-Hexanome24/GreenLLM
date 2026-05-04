## API Documentation

### GET `/carbon`
Returns the mock carbon footprint for each model.

Response shape:
- `request_metrics.input_tokens`: fixed mock input token count
- `models.<model>.output_tokens_estimated`: estimated output token count for the model
- `models.<model>.total_tokens`: input + output tokens for the model
- `models.<model>.carbon_cost_per_token_kg_co2`: carbon cost per token
- `models.<model>.total_carbon_cost_kg_co2`: total carbon cost for the model
- `models_sorted_by_greenest`: models sorted from lowest to highest carbon cost

### GET `/bestLLM`
Placeholder endpoint for future model selection logic.

### Carbon cost formula
`carbon cost = carbon cost per token * (number of tokens in + number of tokens out)`

### Token assumptions
- `tokens in`: fixed mock value for now
- `tokens out`: estimated per model

### Future ranking logic
`utility = w1 * perf + w2 * (1 - carbon cost)`