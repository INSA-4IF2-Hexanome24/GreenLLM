package GreenLLM.app.dto;

public class AuthResponse {

    private Long id;
    private String type;
    private String message;

    public AuthResponse() {
    }

    public AuthResponse(Long id, String type, String message) {
        this.id = id;
        this.type = type;
        this.message = message;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }
}
