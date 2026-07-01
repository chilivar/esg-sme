using Microsoft.AspNetCore.Mvc;
using RecomendationSystem.Services.News;

namespace RecomendationSystem.Controllers
{
    public class NewsController : BaseController
    {
        private readonly IApiNewsService newsService;

        public NewsController(IApiNewsService newsService)
        {
            this.newsService = newsService;
        }

        [HttpGet("GetNews/{companyId}")]
        public async Task<IActionResult> GetNews(int companyId)
        {
            var result = await newsService.GetNewsWithRecommendations(companyId);
            if(result.IsSuccess)
                return Ok(result.Data);
            return BadRequest(result.Message);
        }
    }
}
