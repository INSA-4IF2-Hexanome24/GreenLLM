package GreenLLM.app.dto;

public class AuthResponse {

    private String name;
    private String username;
    private String email;
    private String role; // just "admin" or "employee"
    private String city;
    private String country;
    private String avatar; // may be null

    public AuthResponse() {
    }

    public AuthResponse(Long id, String type, String message) {/*
        this.id = id;
        this.type = type;
        this.message = message;*/
    }
    
    public AuthResponse(String name, String username, String email, String role, String city, String country, String avatar) {
        this.name = name;
        this.username = username;
        this.email = email;
        this.role = role;
        this.city = city;
        this.country = country;
        this.avatar = avatar;
    }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public String getRole() { return role; }
    public void setRole(String role) { this.role = role; }

    public String getCity() { return city; }
    public void setCity(String city) { this.city = city; }

    public String getCountry() { return country; }
    public void setCountry(String country) { this.country = country; }

    public String getAvatar() { return avatar; }
    public void setAvatar(String avatar) { this.avatar = avatar; }
}