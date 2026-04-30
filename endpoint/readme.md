GetCarbonCost
=> carbon cost per model for given request
carbon cost = carbon cost per token * (number of tokens in + number of tokens out)
tokens in = calculate from request
number of tokens out = estimate from request and model

getGreenestModel
=> array of models sorted by utility
utility = w1 * perf + w2 * (1 - carbon cost)