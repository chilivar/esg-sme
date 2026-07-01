using Microsoft.AspNetCore.Mvc;
using RecomendationSystem.Services;

namespace RecomendationSystem.Controllers
{
    public class SwotController : BaseController
    {
        private readonly ISwotService service;

        public SwotController(ISwotService service)
        {
            this.service = service;
        }

        [HttpGet("Swot/{id}")]
        public async Task<IActionResult> Get(int id)
        {
            var result = await service.GetSwot(id);
            return FromResult(result);
        }
    }
}
