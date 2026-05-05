package GreenLLM.app.dto;

import java.math.BigDecimal;

public class RequeteResponse {

    private Long id;
    private String description;
    private int nombreTokens;
    private BigDecimal coutTotal;
    private Long utilisateurId;

    public RequeteResponse() {
    }

    public RequeteResponse(Long id, String description, int nombreTokens, BigDecimal coutTotal, Long utilisateurId) {
        this.id = id;
        this.description = description;
        this.nombreTokens = nombreTokens;
        this.coutTotal = coutTotal;
        this.utilisateurId = utilisateurId;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public int getNombreTokens() {
        return nombreTokens;
    }

    public void setNombreTokens(int nombreTokens) {
        this.nombreTokens = nombreTokens;
    }

    public BigDecimal getCoutTotal() {
        return coutTotal;
    }

    public void setCoutTotal(BigDecimal coutTotal) {
        this.coutTotal = coutTotal;
    }

    public Long getUtilisateurId() {
        return utilisateurId;
    }

    public void setUtilisateurId(Long utilisateurId) {
        this.utilisateurId = utilisateurId;
    }
}
