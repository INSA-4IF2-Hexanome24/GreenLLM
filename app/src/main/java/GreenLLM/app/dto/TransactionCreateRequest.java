package GreenLLM.app.dto;

public class TransactionCreateRequest {

    private Long utilisateurId;
    private Long modelId;
    private Long requeteId;
    private Long reponseId;

    public TransactionCreateRequest() {
    }

    public Long getUtilisateurId() {
        return utilisateurId;
    }

    public void setUtilisateurId(Long utilisateurId) {
        this.utilisateurId = utilisateurId;
    }

    public Long getModelId() {
        return modelId;
    }

    public void setModelId(Long modelId) {
        this.modelId = modelId;
    }

    public Long getRequeteId() {
        return requeteId;
    }

    public void setRequeteId(Long requeteId) {
        this.requeteId = requeteId;
    }

    public Long getReponseId() {
        return reponseId;
    }

    public void setReponseId(Long reponseId) {
        this.reponseId = reponseId;
    }
}
