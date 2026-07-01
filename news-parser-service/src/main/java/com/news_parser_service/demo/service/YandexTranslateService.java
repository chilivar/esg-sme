package com.news_parser_service.demo.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.*;

@Service
public class YandexTranslateService {

    private final RestTemplate restTemplate;

    @Value("${yandex.translate.url}")
    private String url;

    @Value("${yandex.translate.folder-id}")
    private String folderId;

    @Value("${yandex.translate.api-key}")
    private String apiKey;

    public YandexTranslateService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public List<String> translateBatch(List<String> texts, String targetLang) {
        if (isEmpty(texts)) return List.of();

        HttpEntity<Map<String, Object>> request = buildRequest(texts, targetLang);
        Map<String, Object> responseBody = send(request);

        return extractTranslations(responseBody);
    }

    private boolean isEmpty(List<String> texts) {
        return texts == null || texts.isEmpty();
    }

    private HttpEntity<Map<String, Object>> buildRequest(List<String> texts, String targetLang) {
        HttpHeaders headers = buildHeaders();
        Map<String, Object> body = buildBody(texts, targetLang);
        return new HttpEntity<>(body, headers);
    }

    private HttpHeaders buildHeaders() {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        headers.set("Authorization", "Api-Key " + apiKey);
        return headers;
    }

    private Map<String, Object> buildBody(List<String> texts, String targetLang) {
        Map<String, Object> body = new HashMap<>();
        body.put("folderId", folderId);
        body.put("texts", texts);
        body.put("targetLanguageCode", targetLang);
        return body;
    }

    private Map<String, Object> send(HttpEntity<Map<String, Object>> request) {
        ResponseEntity<Map> response = restTemplate.exchange(
                url,
                HttpMethod.POST,
                request,
                Map.class
        );

        Map<?, ?> raw = response.getBody();
        if (raw == null) return Map.of();

        // безопасное приведение Map<?,?> -> Map<String,Object>
        Map<String, Object> result = new HashMap<>();
        for (Map.Entry<?, ?> e : raw.entrySet()) {
            result.put(String.valueOf(e.getKey()), e.getValue());
        }
        return result;
    }

    @SuppressWarnings("unchecked")
    private List<String> extractTranslations(Map<String, Object> responseBody) {
        if (responseBody == null || responseBody.isEmpty()) return List.of();

        Object translationsObj = responseBody.get("translations");
        if (!(translationsObj instanceof List<?> list)) return List.of();

        List<String> out = new ArrayList<>();
        for (Object item : list) {
            if (item instanceof Map<?, ?> map) {
                Object textObj = map.get("text");
                if (textObj != null) out.add(textObj.toString());
            }
        }
        return out;
    }
}