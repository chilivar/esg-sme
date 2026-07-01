package com.news_parser_service.demo.model;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.util.List;

@Data
@AllArgsConstructor
public class YandexTranslateRequest {

    private String folderId;
    private List<String> texts;
    private String targetLanguageCode;
}
