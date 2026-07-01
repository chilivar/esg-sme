using Microsoft.AspNetCore.Mvc;
using RecomendationSystem.Models;
using RecomendationSystem.Services.Answers;

namespace RecomendationSystem.Controllers
{
    public class AnswersController : BaseController
    {
        private readonly IAnswersService service;

        public AnswersController(IAnswersService service)
        {
            this.service = service;
        }

        [HttpPost("Memorize")]
        public async Task<IActionResult> Memorize([FromBody] SurveySubmitDto submit)
        {
            var result = await service.Memorize(submit);
            return FromResult(result);
        }

        [HttpGet("GetByCompany/{id}")]
        public async Task<IActionResult> Get(int id)
        {
            var result = await service.GetByCompanyId(id);
            return FromResult(result);
        }
    }
}
