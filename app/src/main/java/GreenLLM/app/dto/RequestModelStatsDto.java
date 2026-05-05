package GreenLLM.app.dto;



public class RequestModelStatsDto{

    private String name;
    private String power;
    private double performanceScore;
    private double co2CostScore;

    public RequestModelStatsDto() {
    }

    
    public RequestModelStatsDto(String name, String power, double performanceScore, double co2CostScore) {
        this.name = name;
        this.power = power;
        this.performanceScore = performanceScore;
        this.co2CostScore = co2CostScore;
    }

   

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getPower() {
        return power;
    }

    public void setPower(String power) {
        this.power = power;
    }

    public double getPerformanceScore() {
        return performanceScore;
    }

    public void setPerformanceScore(double performanceScore) {
        this.performanceScore = performanceScore;
    }

    public double getCo2CostScore() {
        return co2CostScore;
    }

    public void setCo2CostScore(double co2CostScore) {
        this.co2CostScore = co2CostScore;
    }
}

