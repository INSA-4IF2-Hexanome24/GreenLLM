package GreenLLM.app.dto;

public class CarbonRequestDto {

    private String query;
    private Long utilisateurId;

    public CarbonRequestDto() {
    }

    public String getQuery() {
        return query;
    }

    public void setQuery(String query) {
        this.query = query;
    }

    public Long getUtilisateurId() {
        return utilisateurId;
    }

    public void setUtilisateurId(Long utilisateurId) {
        this.utilisateurId = utilisateurId;
    }
}
