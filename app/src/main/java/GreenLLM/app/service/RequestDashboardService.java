package GreenLLM.app.service;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import GreenLLM.app.model.Entreprise;
import GreenLLM.app.repository.EntrepriseRepository;
import GreenLLM.app.model.ModelLLM;
import GreenLLM.app.repository.ModelLLMRepository;
import GreenLLM.app.repository.RequeteRepository;
import GreenLLM.app.dto.WebSearchAnswerDto;
import GreenLLM.app.dto.RequestDashboardResponse;
import GreenLLM.app.dto.RequestModelStatsDto;
import GreenLLM.app.dto.RouterScoreDto;
import GreenLLM.app.dto.UtilityScoresFastApi;

import java.util.List;
import java.util.ArrayList;



@Service
public class RequestDashboardService {

    private final ModelLLMRepository modelRepository;
    private final RequeteRepository requeteRepository;
    private final RestClient fastapiClient;

    public RequestDashboardService(ModelLLMRepository modelRepo, RequeteRepository requeteRepo, RestClient fastapiClient) {
        this.modelRepository = modelRepo;
        this.requeteRepository = requeteRepo;
        this.fastapiClient = fastapiClient;
    }

    /*
    public RequestDashboardResponse getLlmComparison() {
        RequestDashboardResponse response = new RequestDashboardResponse();
        List<RequestModelStatsDto> listStats = new ArrayList<>();

        List<ModelLLM> activeModels = modelRepository.findAll();

        for (ModelLLM model : activeModels) {
            RequestModelStatsDto stats = new RequestModelStatsDto();
            stats.setName(model.getNom());
            
            //TO DO : get data from endpoint with router 
            //and update stats attributes

            listStats.add(stats); 
        }

        response.setStatsPerModel(listStats);
        
        return response;
    }*/

    public RequestDashboardResponse getLlmComparison(String queryText) {

        UtilityScoresFastApi responseFastAPI = fastapiClient.get()
                .uri(uriBuilder -> uriBuilder
                        .path("/utility-scores")
                        .queryParam("query", queryText)
                        .build())
                .retrieve()
                .body(UtilityScoresFastApi.class);

        if (responseFastAPI == null) {
            return new RequestDashboardResponse(List.of());
        }

        
        if ("web_search".equals(responseFastAPI.getBest_model())) {
            List<WebSearchAnswerDto> answers = responseFastAPI.getAnswers() != null
                    ? responseFastAPI.getAnswers()
                    : List.of();
            return new RequestDashboardResponse(answers, true);
        }

        
        List<RequestModelStatsDto> statsList = new ArrayList<>();

        if (responseFastAPI.getRouters() != null) {
            for (RouterScoreDto router : responseFastAPI.getRouters()) {
                RequestModelStatsDto dto = new RequestModelStatsDto();
                dto.setName(router.getModel());
                dto.setPerformanceScore(router.getPerformance());
                dto.setCo2CostScore(router.getCo2());

                double perf = router.getPerformance();
                String power = perf >= 0.7 ? "High" : perf >= 0.4 ? "Medium" : "Low";
                dto.setPower(power);

                statsList.add(dto);
            }
        }

        return new RequestDashboardResponse(statsList);
    }
}