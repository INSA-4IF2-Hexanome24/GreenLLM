package GreenLLM.app.dto;

import java.util.List;

public class UtilityScoresFastApi {
    private List<RouterScoreDto> routers;
    private double difficulty_score;
    private double threshold;
    private String best_model;

    public UtilityScoresFastApi(){}

    public List<RouterScoreDto> getRouters() { return routers; }
    public void setRouters(List<RouterScoreDto> routers) { this.routers = routers; }
    public double getDifficulty_score() { return difficulty_score; }
    public void setDifficulty_score(double difficulty_score) { this.difficulty_score = difficulty_score; }
    public double getThreshold() { return threshold; }
    public void setThreshold(double threshold) { this.threshold = threshold; }
    public String getBest_model() { return best_model; }
    public void setBest_model(String best_model) { this.best_model = best_model; }
}