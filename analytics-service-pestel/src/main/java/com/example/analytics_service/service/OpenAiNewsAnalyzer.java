package com.example.analytics_service.service;

import com.example.analytics_service.model.News;
import com.example.analytics_service.model.NewsAnalysisResult;
import com.example.analytics_service.model.NewsAnalyzer;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

@Service
public class OpenAiNewsAnalyzer implements NewsAnalyzer {

    private final RestTemplate restTemplate;
    private final ObjectMapper objectMapper;
    private final String apiKey;
    private final String model;
    private final String url;

    public OpenAiNewsAnalyzer(
            RestTemplate restTemplate,
            ObjectMapper objectMapper,
            @Value("${openai.api-key}") String apiKey,
            @Value("${openai.model}") String model,
            @Value("${openai.url}") String url
    ) {
        this.restTemplate = restTemplate;
        this.objectMapper = objectMapper;
        this.apiKey = apiKey;
        this.model = model;
        this.url = url;
    }

    @Override
    public List<NewsAnalysisResult> analyzeBatch(List<News> newsList) {
        if (newsList == null || newsList.isEmpty()) {
            return List.of();
        }

        try {
            String requestBody = buildBatchRequestBody(newsList);

            HttpHeaders headers = new HttpHeaders();
            headers.setBearerAuth(apiKey);
            headers.setContentType(MediaType.APPLICATION_JSON);

            HttpEntity<String> request = new HttpEntity<>(requestBody, headers);

            ResponseEntity<String> response = restTemplate.exchange(
                    url,
                    HttpMethod.POST,
                    request,
                    String.class
            );

            String responseBody = response.getBody();
            JsonNode root = objectMapper.readTree(responseBody);

            String content = root.path("choices")
                    .path(0)
                    .path("message")
                    .path("content")
                    .asText();

            JsonNode resultRoot = objectMapper.readTree(cleanJson(content));
            JsonNode items = resultRoot.path("items");

            if (!items.isArray()) {
                throw new RuntimeException("OpenAI вернул JSON без массива items: " + content);
            }

            List<JsonNode> sortedItems = new ArrayList<>();

            for (JsonNode item : items) {
                sortedItems.add(item);
            }

            sortedItems.sort((a, b) ->
                    Integer.compare(a.path("index").asInt(), b.path("index").asInt())
            );

            List<NewsAnalysisResult> results = new ArrayList<>();

            for (JsonNode item : sortedItems) {
                String pestelType = item.path("pestelType").asText();
                String impactType = item.path("impactType").asText();
                BigDecimal impactStrength = item.path("impactStrength").decimalValue();

                List<String> sdgCodes = new ArrayList<>();
                for (JsonNode sdg : item.path("sdgCodes")) {
                    sdgCodes.add(sdg.asText());
                }

                results.add(new NewsAnalysisResult(
                        pestelType,
                        impactType,
                        impactStrength,
                        sdgCodes
                ));
            }

            if (results.size() != newsList.size()) {
                throw new RuntimeException(
                        "Количество результатов не совпадает с количеством новостей. " +
                                "Ожидалось: " + newsList.size() + ", получено: " + results.size()
                );
            }

            return results;

        } catch (Exception e) {
            throw new RuntimeException("Ошибка при пакетном анализе новостей через OpenAI REST API", e);
        }
    }

    private String cleanJson(String text) {
        if (text == null) {
            return "";
        }

        text = text.trim();

        if (text.startsWith("```json")) {
            text = text.substring(7).trim();
        } else if (text.startsWith("```")) {
            text = text.substring(3).trim();
        }

        if (text.endsWith("```")) {
            text = text.substring(0, text.length() - 3).trim();
        }

        return text;
    }

    private String buildBatchRequestBody(List<News> newsList) throws Exception {
        String systemPrompt = """
    Ты анализируешь заголовки новостей на русском языке.
    Верни только валидный JSON.
    Не используй markdown.
    Не добавляй пояснения, комментарии или текст вне JSON.

    Формат ответа:
    {
      "items": [
        {
          "index": 0,
          "pestelType": "POLITICAL|ECONOMIC|SOCIAL|TECHNOLOGICAL|ENVIRONMENTAL|LEGAL",
          "impactType": "THREAT|OPPORTUNITY",
          "impactStrength": 0.00,
          "sdgCodes": ["8", "7"]
        }
      ]
    }

    Правила:
    - Верни строго по одному объекту на каждый входной заголовок
    - index должен совпадать с номером новости во входном списке
    - порядок объектов должен соответствовать порядку входных новостей
    - pestelType должен быть только один
    - impactType только THREAT или OPPORTUNITY
    - impactStrength должен быть числом от 0 до 1
    - sdgCodes должен содержать от 0 до 3 значений
    - В sdgCodes указывай только номера ЦУР: 1,3,4,5,6,7,8,9,10,12,13,15,16,17
    - Выбирай ЦУР только если тема новости прямо и явно соответствует цели
    - Обязательно должен быть хотя бы один ЦУР
    - ЦУР 8 ставь только если новость прямо про занятость, рабочие места, рынок труда, производительность, экономический рост, бизнес-активность, доходы от труда
    - Если новость больше относится к регулированию, закону, госуправлению, проверкам, налогам или институтам, чаще подходит 16, а не 8
    - Если новость про инновации, технологии, цифровизацию, промышленность, инфраструктуру, производство, чаще подходит 9, а не 8
    - Если новость про энергетику, энергоэффективность, электричество, ВИЭ, топливо, чаще подходит 7
    - Если новость про экологию, выбросы, климат, отходы, декарбонизацию, чаще подходят 12 и 13
    - Если новость про образование и обучение, чаще подходит 4
    - Если новость про здоровье, медицину, безопасность труда, чаще подходит 3
    - Если новость про воду, водоснабжение, канализацию, очистку воды, чаще подходит 6
    - Если новость про неравенство, социальную поддержку уязвимых групп, чаще подходит 10
    - Если новость про леса, почвы, биоразнообразие, землю, подходит 15
    - Если новость про международное сотрудничество, совместные программы, партнёрства, подходит 17

    Держи список ЦУР:
    1. Ликвидация нищеты
    3. Хорошее здоровье и благополучие
    4. Качественное образование
    5. Гендерное равенство
    6. Чистая вода и санитария
    7. Недорогостоящая и чистая энергия
    8. Достойная работа и экономический рост
    9. Индустриализация, инновации и инфраструктура
    10. Уменьшение неравенства
    12. Ответственное потребление и производство
    13. Борьба с изменением климата
    15. Сохранение экосистем суши
    16. Мир, правосудие и эффективные институты
    17. Партнёрства в интересах устойчивого развития

    Правила для PESTEL:
    - если новость про субсидии, госпрограммы, господдержку -> POLITICAL
    - если про инфляцию, тарифы, ставки, кредиты -> ECONOMIC
    - если про зарплаты, кадры, здоровье, образование -> SOCIAL
    - если про ИИ, цифровизацию, автоматизацию, киберриски -> TECHNOLOGICAL
    - если про выбросы, отходы, климат, экологию -> ENVIRONMENTAL
    - если про налоги, законы, проверки, кодексы -> LEGAL
    """;

        StringBuilder userPrompt = new StringBuilder("Проанализируй заголовки новостей:\n\n");

        for (int i = 0; i < newsList.size(); i++) {
            String title = newsList.get(i).getTitle();
            userPrompt.append(i)
                    .append(". ")
                    .append(title == null ? "" : title)
                    .append("\n");
        }

        ObjectNode body = objectMapper.createObjectNode();
        body.put("model", model);
        body.put("temperature", 0);
        body.put("max_tokens", 8000);

        ArrayNode messages = body.putArray("messages");

        messages.addObject()
                .put("role", "system")
                .put("content", systemPrompt);

        messages.addObject()
                .put("role", "user")
                .put("content", userPrompt.toString());

        return objectMapper.writeValueAsString(body);
    }
}