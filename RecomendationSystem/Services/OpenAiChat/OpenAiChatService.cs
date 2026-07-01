using RecomendationSystem.Models.Entities;
using RecomendationSystem.Services.Answers;
using System.Text.Json;

namespace RecomendationSystem.Services.OpenAiChat
{
    public class OpenAiChatService
    {
        private readonly IHttpClientFactory _httpClientFactory;
        private readonly IConfiguration _config;
        private readonly IAnswersService service;
        public OpenAiChatService(IHttpClientFactory httpClientFactory, IConfiguration config, IAnswersService service)
        {
            _httpClientFactory = httpClientFactory;
            _config = config;
            this.service = service;
        }

        public async Task<string> AskAsync(int id, string language, CancellationToken ct = default)
        {
            var client = _httpClientFactory.CreateClient("OpenAI");
            var model = _config["OpenAI:Model"] ?? "gpt-4.1-mini";

            var json = await service.GetByCompanyId(id);
            var userText = JsonSerializer.Serialize(json);
            string LANGUAGE = "";
            if (language == "ru")
                LANGUAGE = "РУССКОМ";
            else if (language == "en")
                LANGUAGE = "АНГЛИЙСКОМ";
            else if (language == "kz")
                LANGUAGE = "КАЗАХСКОМ";
                var payload = new
                {
                    model,
                    messages = new object[]
                    {
                    new {
                        role = "system",
                        content =
                        @"Ты — консультант по целям устойчивого развития (ЦУР/SDGs).
                        Держи эти 17 ЦУР
                        1.Ликвидация нищеты.
                        2.Ликвидация голода.
                        3. Хорошее здоровье и благополучие.
                        4. Качественное образование.
                        5. Гендерное равенство.
                        6. Чистая вода и санитария.
                        7. Недорогостоящая и чистая энергия.
                        8. Достойная работа и экономический рост.
                        9. Индустриализация, инновации и инфраструктура.
                        10. Уменьшение неравенства.
                        11. Устойчивые города и населенные пункты.
                        12. Ответственное потребление и производство.
                        13. Борьба с изменением климата.
                        14. Сохранение морских экосистем.
                        15. Сохранение экосистем суши.
                        16. Мир, правосудие и эффективные институты.
                        17. Партнерства в интересах устойчивого развития.
                        Категории и относящиеся к ним ЦУР:
                        Economic: 8, 9, 12
                        Social: 1, 3, 4, 5, 8, 10
                        Environmental: 6, 7, 12, 13, 15
                        Technological: 9, 12, 8, 4
                        Теперь правила:
                        1) Не придумывай факты о компании. Используй только входной JSON.
                        2) Не нужно повторять содержимое JSON в ответе, просто дай рекомендации по улучшению.
                        3) Для каждой категории оцени влияние связанных с ней ЦУР на категорию.
                        4) При анализе учитывай, что ЦУР, расположенные раньше в списке категории, имеют больший приоритет и больший вес.
                        5) Ответ должен быть строго на " + LANGUAGE + """
                        Формат ответа:
                        Краткий общий вывод.
                        Анализ ЦУР.
                        Анализ категорий:
                        Economic
                        Social
                        Environmental
                        Technological
                        Для каждой категории:
                        уровень влияния ЦУР,
                        сильные стороны,
                        слабые стороны,
                        рекомендации.
                        Итоговые рекомендации компании.
                        """

                    },
                    new {
                        role = "user",
                        content = userText
                    }
                    }
                };

            using var resp = await client.PostAsJsonAsync("chat/completions", payload, ct);

            var body = await resp.Content.ReadFromJsonAsync<ChatCompletionsResponse>(cancellationToken: ct);
            if (!resp.IsSuccessStatusCode)
            {
                var raw = await resp.Content.ReadAsStringAsync(ct);
                throw new HttpRequestException($"OpenAI error {(int)resp.StatusCode}: {raw}");
            }

            return body?.choices?.FirstOrDefault()?.message?.content?.Trim()
                   ?? "(empty response)";
        }

        public async Task<string> AskAsync1(string language, List<Sdg> sdgs, List<Category> categories)
        {
            CancellationToken ct = default;
            var client = _httpClientFactory.CreateClient("OpenAI");
            var model = _config["OpenAI:Model"] ?? "gpt-4.1-mini";

            var json = new
            {
                Sdgs = sdgs,
                Categories = categories
            };

            var userText = JsonSerializer.Serialize(json);
            string LANGUAGE = "";
            if (language == "ru")
                LANGUAGE = "РУССКОМ";
            else if (language == "en")
                LANGUAGE = "АНГЛИЙСКОМ";
            else if (language == "kz")
                LANGUAGE = "КАЗАХСКОМ";
            var payload = new
            {
                model,
                messages = new object[]
                {
                    new {
                        role = "system",
                        content =
                        @"Ты — консультант по целям устойчивого развития (ЦУР/SDGs).
                        Держи эти 17 ЦУР
                        1.Ликвидация нищеты.
                        2.Ликвидация голода.
                        3. Хорошее здоровье и благополучие.
                        4. Качественное образование.
                        5. Гендерное равенство.
                        6. Чистая вода и санитария.
                        7. Недорогостоящая и чистая энергия.
                        8. Достойная работа и экономический рост.
                        9. Индустриализация, инновации и инфраструктура.
                        10. Уменьшение неравенства.
                        11. Устойчивые города и населенные пункты.
                        12. Ответственное потребление и производство.
                        13. Борьба с изменением климата.
                        14. Сохранение морских экосистем.
                        15. Сохранение экосистем суши.
                        16. Мир, правосудие и эффективные институты.
                        17. Партнерства в интересах устойчивого развития.
                        Категории и относящиеся к ним ЦУР:
                        Economic: 8, 9, 12
                        Social: 1, 3, 4, 5, 8, 10
                        Environmental: 6, 7, 12, 13, 15
                        Technological: 9, 12, 8, 4
                        Теперь правила:
                        1) Не придумывай факты о компании. Используй только входной JSON.
                        2) Не нужно повторять содержимое JSON в ответе, просто дай рекомендации по улучшению.
                        3) Для каждой категории оцени влияние связанных с ней ЦУР на категорию.
                        4) При анализе учитывай, что ЦУР, расположенные раньше в списке категории, имеют больший приоритет и больший вес.
                        5) Ответ должен быть строго на " + LANGUAGE
                    },
                    new {
                        role = "user",
                        content = userText
                    }
                }
            };

            using var resp = await client.PostAsJsonAsync("chat/completions", payload, ct);

            var body = await resp.Content.ReadFromJsonAsync<ChatCompletionsResponse>(cancellationToken: ct);
            if (!resp.IsSuccessStatusCode)
            {
                var raw = await resp.Content.ReadAsStringAsync(ct);
                throw new HttpRequestException($"OpenAI error {(int)resp.StatusCode}: {raw}");
            }

            return body?.choices?.FirstOrDefault()?.message?.content?.Trim()
                   ?? "(empty response)";
        }

        // минимальные DTO под ответ
        public sealed class ChatCompletionsResponse
        {
            public Choice[]? choices { get; set; }
            public sealed class Choice
            {
                public Message? message { get; set; }
            }
            public sealed class Message
            {
                public string? content { get; set; }
            }
        }
    }
}
