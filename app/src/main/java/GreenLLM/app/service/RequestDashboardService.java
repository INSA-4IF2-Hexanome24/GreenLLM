package GreenLLM.app.service;

import org.springframework.stereotype.Service;

import GreenLLM.app.model.Entreprise;
import GreenLLM.app.repository.EntrepriseRepository;
import GreenLLM.app.model.ModelLLM;
import GreenLLM.app.repository.ModelLLMRepository;
import GreenLLM.app.repository.RequeteRepository;

import GreenLLM.app.dto.RequestDashboardResponse;
import GreenLLM.app.dto.RequestModelStatsDto;

import java.util.List;
import java.util.ArrayList;



@Service
public class RequestDashboardService {

    private final ModelLLMRepository modelRepository;
    private final RequeteRepository requeteRepository; 

    public RequestDashboardService(ModelLLMRepository modelRepo, RequeteRepository requeteRepo) {
        this.modelRepository = modelRepo;
        this.requeteRepository = requeteRepo;
    }

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
    }
}