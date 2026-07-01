package com.send_message.mail_service.dto;

public class TemplateMailRequest {

    private String email;
    private String username;
    private String link;

    public TemplateMailRequest() {
    }

    public TemplateMailRequest(String email, String username, String link) {
        this.email = email;
        this.username = username;
        this.link = link;
    }

    public String getEmail() {
        return email;
    }

    public String getUsername() {
        return username;
    }

    public String getLink() {
        return link;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public void setLink(String link) {
        this.link = link;
    }
}
