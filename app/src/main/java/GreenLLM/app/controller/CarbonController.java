package GreenLLM.app.controller;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestClient;

import GreenLLM.app.dto.CarbonRequestDto;
import GreenLLM.app.model.ModelLLM;
import GreenLLM.app.model.Reponse;
import GreenLLM.app.model.Requete;
import GreenLLM.app.model.Utilisateur;
import GreenLLM.app.repository.ModelLLMRepository;
import GreenLLM.app.repository.ReponseRepository;
import GreenLLM.app.repository.RequeteRepository;
import GreenLLM.app.repository.UtilisateurRepository;

@RestController
@RequestMapping("/api/carbon")
public class CarbonController {

    private final RestClient fastapiClient;
    private final RequeteRepository requeteRepository;
    private final UtilisateurRepository utilisateurRepository;
    private final ReponseRepository reponseRepository;
    private final ModelLLMRepository modelLLMRepository;

    public CarbonController(RestClient fastapiClient,
                            RequeteRepository requeteRepository,
                            UtilisateurRepository utilisateurRepository,
                            ReponseRepository reponseRepository,
                            ModelLLMRepository modelLLMRepository) {
        this.fastapiClient = fastapiClient;
        this.requeteRepository = requeteRepository;
        this.utilisateurRepository = utilisateurRepository;
        this.reponseRepository = reponseRepository;
        this.modelLLMRepository = modelLLMRepository;
    }

    @GetMapping
    public ResponseEntity<Map<String, Object>> getCarbonFootprint(@RequestParam String query) {
        return ResponseEntity.ok(appelerEndpointCarbon(query));
    }

    @PostMapping
    public ResponseEntity<Map<String, Object>> creerRequeteEtCalculerCarbon(@RequestBody CarbonRequestDto request) {
        Utilisateur utilisateur = utilisateurRepository.findById(request.getUtilisateurId())
                .orElseThrow(() -> new IllegalArgumentException("Utilisateur introuvable"));

        Map<String, Object> carbonResponse = appelerEndpointCarbon(request.getQuery());
        int inputTokens = extraireInputTokens(carbonResponse);

        Requete requete = new Requete(request.getQuery(), utilisateur, inputTokens);
        Requete savedRequete = requeteRepository.save(requete);
        List<Map<String, Object>> reponses = creerReponsesParModele(carbonResponse);

        Map<String, Object> response = new LinkedHashMap<>();
        response.put("requeteId", savedRequete.getId());
        response.put("utilisateurId", utilisateur.getId());
        response.put("inputTokens", savedRequete.getNombreTokens());
        response.put("reponses", reponses);
        response.put("carbon", carbonResponse);

        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    private Map<String, Object> appelerEndpointCarbon(String query) {
        return fastapiClient.get()
                .uri(uriBuilder -> uriBuilder
                        .path("/carbon")
                        .queryParam("query", query)
                        .build())
                .retrieve()
                .body(new ParameterizedTypeReference<Map<String, Object>>() {
                });
    }

    @SuppressWarnings("unchecked")
    private int extraireInputTokens(Map<String, Object> carbonResponse) {
        Object requestMetrics = carbonResponse.get("request_metrics");
        if (!(requestMetrics instanceof Map<?, ?>)) {
            return 0;
        }

        Object inputTokens = ((Map<String, Object>) requestMetrics).get("input_tokens");
        if (inputTokens instanceof Number number) {
            return number.intValue();
        }

        return 0;
    }

    @SuppressWarnings("unchecked")
    private List<Map<String, Object>> creerReponsesParModele(Map<String, Object> carbonResponse) {
        List<Map<String, Object>> reponses = new ArrayList<>();
        Object models = carbonResponse.get("models");
        if (!(models instanceof Map<?, ?>)) {
            return reponses;
        }

        for (Map.Entry<String, Object> entry : ((Map<String, Object>) models).entrySet()) {
            if (!(entry.getValue() instanceof Map<?, ?>)) {
                continue;
            }

            String nomModele = entry.getKey();
            Map<String, Object> modelMetrics = (Map<String, Object>) entry.getValue();
            int outputTokens = extraireEntier(modelMetrics.get("output_tokens_estimated"));
            BigDecimal carbonParToken = extraireBigDecimal(modelMetrics.get("carbon_cost_per_token_kg_co2"));
            ModelLLM modelLLM = chercherOuCreerModele(nomModele, carbonParToken);

            Reponse reponse = new Reponse("Reponse estimee pour " + nomModele, outputTokens);
            reponse.setModelUtilise(modelLLM);
            Reponse savedReponse = reponseRepository.save(reponse);

            Map<String, Object> reponseDto = new LinkedHashMap<>();
            reponseDto.put("reponseId", savedReponse.getId());
            reponseDto.put("modelId", modelLLM.getId());
            reponseDto.put("model", modelLLM.getNom());
            reponseDto.put("outputTokens", savedReponse.getNombreTokens());
            reponses.add(reponseDto);
        }

        return reponses;
    }

    private ModelLLM chercherOuCreerModele(String nomModele, BigDecimal carbonParToken) {
        return modelLLMRepository.findByNomIgnoreCase(nomModele)
                .map(modele -> completerCoutModeleSiAbsent(modele, carbonParToken))
                .orElseGet(() -> modelLLMRepository.save(
                        new ModelLLM(nomModele, carbonParToken.doubleValue(), carbonParToken)));
    }

    private ModelLLM completerCoutModeleSiAbsent(ModelLLM modele, BigDecimal coutParToken) {
        if (modele.getCoutParToken() == null || modele.getCoutParToken().compareTo(BigDecimal.ZERO) == 0) {
            modele.setCoutParToken(coutParToken);
            return modelLLMRepository.save(modele);
        }

        return modele;
    }

    private int extraireEntier(Object valeur) {
        if (valeur instanceof Number number) {
            return number.intValue();
        }

        return 0;
    }

    private BigDecimal extraireBigDecimal(Object valeur) {
        if (valeur instanceof Number number) {
            return BigDecimal.valueOf(number.doubleValue());
        }

        return BigDecimal.ZERO;
    }
}
