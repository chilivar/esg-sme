using Microsoft.AspNetCore.Mvc;
using RecomendationSystem.Models;
using RecomendationSystem.Services;
using RecomendationSystem.Services.Answers;
using RecomendationSystem.Services.Forecast;
using RecomendationSystem.Services.News;
using RecomendationSystem.Services.OpenAiChat;
using System;
using System.ComponentModel.Design;

namespace RecomendationSystem.Controllers
{
    public class UnityController : BaseController
    {
        private readonly IAnswersService answersService;
        private readonly IApiNewsService newsService;
        private readonly IMultiYearForecastService forecastService;
        private readonly ISwotService swotService;
        private readonly OpenAiChatService chatService;
        private readonly ICategoriesService categoriesService;
        public UnityController(IAnswersService answersService, IApiNewsService newsService, IMultiYearForecastService forecastService, ISwotService swotService, OpenAiChatService chatService, ICategoriesService categoriesService)
        {
            this.answersService = answersService;
            this.newsService = newsService;
            this.forecastService = forecastService;
            this.swotService = swotService;
            this.chatService = chatService;
            this.categoriesService = categoriesService;
        }

        [HttpPost("GetResults")]
        public async Task<IActionResult> GetResultsAsync([FromBody] SurveySubmitDto submit, string language)
        {
            var result = answersService.GetResults(submit);
            var newsResult = (await newsService.GetNewsWithRecommendations1(result)).Data;
            var categories = categoriesService.GetResults(result, language);
            var swotResult = await swotService.GetSwot1(result);
            var options = new MultiYearForecastOptions
            {
                Years = 4,
                StartYear = DateTime.UtcNow.Year,
                ThreatSensitivity = 0.10,
                ThreatGrowth = 1.05,
                ActionDecay = 0.85,
                BaseK = 0.50,
                OptimisticK = 1.00,
                NegativeK = 1.20,
                TopSdgCount = 5,
            };
            var chart = forecastService.BuildMultiYearForecast(swotResult.Data, options);

            if (language == "ru" || language == "kz" || language == "en")
            {
                var answer = await chatService.AskAsync1(language, result, categories);
                var questionnaire_id = submit.QuestionnaireId;
                var news = newsResult.News;
                var recommendedSdgs = newsResult.RecommendedSdgs;
                return Ok(new {
                    questionnaire_id,
                    result,
                    categories,
                    news,
                    recommendedSdgs,
                    chart,
                    answer
                });
            }
            else 
                return BadRequest();
        }
    }
}
