package GreenLLM.app.dto;

import java.math.BigDecimal;

public class CoutEconomiseResponse {

    private Long modelId;
    private Long requeteId;
    private Long reponseId;
    private BigDecimal coutEconomise;

    public CoutEconomiseResponse() {
    }

    public CoutEconomiseResponse(Long modelId, Long requeteId, Long reponseId, BigDecimal coutEconomise) {
        this.modelId = modelId;
        this.requeteId = requeteId;
        this.reponseId = reponseId;
        this.coutEconomise = coutEconomise;
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

    public BigDecimal getCoutEconomise() {
        return coutEconomise;
    }

    public void setCoutEconomise(BigDecimal coutEconomise) {
        this.coutEconomise = coutEconomise;
    }
}
