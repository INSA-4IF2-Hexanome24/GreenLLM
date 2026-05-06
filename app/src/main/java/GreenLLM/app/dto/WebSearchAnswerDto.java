package GreenLLM.app.dto;

public class WebSearchAnswerDto {

    private String answer;
    private String source;
    private double score;

    public WebSearchAnswerDto() {}

    public String getAnswer() { return answer; }
    public void setAnswer(String answer) { this.answer = answer; }

    public String getSource() { return source; }
    public void setSource(String source) { this.source = source; }

    public double getScore() { return score; }
    public void setScore(double score) { this.score = score; }
}
