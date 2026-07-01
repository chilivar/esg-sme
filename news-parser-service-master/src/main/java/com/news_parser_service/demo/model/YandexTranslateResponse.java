package com.news_parser_service.demo.model;

import lombok.Data;

import java.util.List;

@Data
public class YandexTranslateResponse {

    private List<TranslatedText> translations;

    @Data
    public static class TranslatedText {
        private String text;
    }
}
