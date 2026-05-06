package GreenLLM.app.dto;

import com.fasterxml.jackson.annotation.JsonAlias;

public class RequeteCreateRequest {

    private String description;
    private Long utilisateurId;
    @JsonAlias({"nbre_de_token", "nbre_tokens", "nombre_tokens", "input_tokens"})
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
