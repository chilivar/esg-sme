using Microsoft.AspNetCore.Mvc;
using RecomendationSystem.Services;
using RecomendationSystem.Services.Forecast;

namespace RecomendationSystem.Controllers
{
    public class ForecastController : BaseController
    {
        private readonly IMultiYearForecastService forecastService;
        private readonly ISwotService swotService;

        public ForecastController(IMultiYearForecastService forecastService, ISwotService swotService)
        {
            this.forecastService = forecastService;
            this.swotService = swotService;
        }

        [HttpGet("multiyear/{companyId:int}")]
        public async Task<ActionResult<MultiYearForecastChartDto>> MultiYear(int companyId)
        {
            var swotResult = await swotService.GetSwot(companyId);
            if (!swotResult.IsSuccess || swotResult.Data is null)
            {
                return BadRequest(swotResult.Message);
            }

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
                ActionDeltaBySdg = new Dictionary<int, double>
                {
                    [5] = 0.12,
                    [8] = 0.10,
                    [12] = 0.15,
                    [7] = 0.12,
                    [13] = 0.12
                }
            };

            var chart = forecastService.BuildMultiYearForecast(swotResult.Data, options);
            return Ok(chart);
        }
    }
}
