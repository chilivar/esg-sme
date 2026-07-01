namespace RecomendationSystem.Services.Forecast;

public sealed class MultiYearForecastChartDto
{
    public string[] Labels { get; init; } = Array.Empty<string>();
    public List<ScenarioLineDto> Series { get; init; } = new();
}
