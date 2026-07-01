namespace RecomendationSystem.Services.Forecast;

public sealed class MultiYearForecastOptions
{
    public int Years { get; init; } = 4;
    public int StartYear { get; init; } = DateTime.UtcNow.Year;
    public double ThreatSensitivity { get; init; } = 0.10;
    public double BaseK { get; init; } = 0.50;
    public double OptimisticK { get; init; } = 1.00;
    public double NegativeK { get; init; } = 1.20;
    public Dictionary<int, double> ActionDeltaBySdg { get; init; } = new();
    public double DefaultActionDelta { get; init; } = 0.12;
    public double ActionDecay { get; init; } = 0.85;
    public double ThreatGrowth { get; init; } = 1.05;
    public int TopSdgCount { get; init; } = 5;
}
