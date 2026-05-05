package GreenLLM.app.dto;


import java.util.List;

public class RequestDashboardResponse {

    private List<RequestModelStatsDto> statsPerModel;

    public RequestDashboardResponse() {
    }

    public RequestDashboardResponse(List<RequestModelStatsDto> statsPerModel) {
        this.statsPerModel = statsPerModel;
    }


    public List<RequestModelStatsDto> getStatsPerModel() {
        return statsPerModel;
    }

    public void setStatsPerModel(List<RequestModelStatsDto> statsPerModel) {
        this.statsPerModel = statsPerModel;
    }
}