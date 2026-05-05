package GreenLLM.app.dto;

public class RouterScoreDto {
    private String model;
    private double utility;
    private double performance;
    private double co2;

    public String getModel() { return model; }
    public void setModel(String model) { this.model = model; }
    public double getUtility() { return utility; }
    public void setUtility(double utility) { this.utility = utility; }
    public double getPerformance() { return performance; }
    public void setPerformance(double performance) { this.performance = performance; }
    public double getCo2() { return co2; }
    public void setCo2(double co2) { this.co2 = co2; }
}