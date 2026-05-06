package GreenLLM.app.dto;

import java.util.List;

public class RequestDashboardResponse {

    private List<RequestModelStatsDto> statsPerModel;
    private boolean webSearch;                  
    private List<WebSearchAnswerDto> answers;   

    public RequestDashboardResponse() {}

    public RequestDashboardResponse(List<RequestModelStatsDto> statsPerModel) {
        this.statsPerModel = statsPerModel;
        this.webSearch = false;
    }

    public RequestDashboardResponse(List<WebSearchAnswerDto> answers, boolean webSearch) {
        this.statsPerModel = List.of();
        this.answers = answers;
        this.webSearch = webSearch;
    }

    public List<RequestModelStatsDto> getStatsPerModel() { return statsPerModel; }
    public void setStatsPerModel(List<RequestModelStatsDto> statsPerModel) { this.statsPerModel = statsPerModel; }

    public boolean isWebSearch() { return webSearch; }
    public void setWebSearch(boolean webSearch) { this.webSearch = webSearch; }

    public List<WebSearchAnswerDto> getAnswers() { return answers; }
    public void setAnswers(List<WebSearchAnswerDto> answers) { this.answers = answers; }
}