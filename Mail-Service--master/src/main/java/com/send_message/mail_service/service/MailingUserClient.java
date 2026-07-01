package com.send_message.mail_service.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.List;

@Service
public class MailingUserClient {

    private final RestTemplate restTemplate;

    @Value("${mailing.users.url}")
    private String mailingUsersUrl;

    @Value("${mailing.users.api-key}")
    private String apiKey;

    public MailingUserClient(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public List<String> getMailingUsers() {
        HttpHeaders headers = new HttpHeaders();
        headers.set("x-api-key", apiKey);

        HttpEntity<Void> entity = new HttpEntity<>(headers);

        ResponseEntity<List<String>> response = restTemplate.exchange(
                mailingUsersUrl,
                HttpMethod.GET,
                entity,
                new ParameterizedTypeReference<List<String>>() {}
        );

        return response.getBody() == null ? List.of() : response.getBody();
    }
}
