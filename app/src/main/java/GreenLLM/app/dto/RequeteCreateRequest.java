package GreenLLM.app.dto;

public class RequeteCreateRequest {

    private String description;
    private Long utilisateurId;
    private int nombreTokens;

    public RequeteCreateRequest() {
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public Long getUtilisateurId() {
        return utilisateurId;
    }

    public void setUtilisateurId(Long utilisateurId) {
        this.utilisateurId = utilisateurId;
    }

    public int getNombreTokens() {
        return nombreTokens;
    }

    public void setNombreTokens(int nombreTokens) {
        this.nombreTokens = nombreTokens;
    }
}
