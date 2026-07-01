using RecomendationSystem.Models;

namespace RecomendationSystem.Services.Forecast;

public interface IMultiYearForecastService
{
    MultiYearForecastChartDto BuildMultiYearForecast(SwotResult swotResult, MultiYearForecastOptions? options = null);
}
