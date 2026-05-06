package GreenLLM.app.service;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import GreenLLM.app.model.Entreprise;
import GreenLLM.app.repository.EntrepriseRepository;
import GreenLLM.app.model.ModelLLM;
import GreenLLM.app.repository.ModelLLMRepository;
import GreenLLM.app.repository.RequeteRepository;

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
            
            // 1. Llamada GET a FastAPI pasándole el query parameter
            UtilityScoresFastApi responseFastAPI = fastapiClient.get()
                    .uri(uriBuilder -> uriBuilder
                            .path("/utility-scores")
                            .queryParam("query", queryText) // Añade ?query=... a la URL
                            .build())
                    .retrieve()
                    .body(UtilityScoresFastApi.class); // Spring convierte el JSON a esta clase

            // 2. Mapear los datos de FastAPI a tu DTO del Front
            List<RequestModelStatsDto> statsList = new ArrayList<>();
            
            // Verificamos que no sea nulo por seguridad
            if (responseFastAPI != null && responseFastAPI.getRouters() != null) {
                for (RouterScoreDto router : responseFastAPI.getRouters()) {
                    RequestModelStatsDto dto = new RequestModelStatsDto();
                    
                    dto.setName(router.getModel()); // Mapea 'model' a 'name'
                    dto.setPerformanceScore(router.getPerformance()); // Mapea 'performance'
                    dto.setCo2CostScore(router.getCo2()); // Mapea 'co2'
                    
                    // Convierto la utilidad (double) a String para el campo 'power' que me pasaste antes
                    //dto.setPower(String.valueOf(router.getUtility())); 
                    
                    statsList.add(dto);
                }
            }

            // 3. Retornamos el objeto final
            return new RequestDashboardResponse(statsList);
        }
}