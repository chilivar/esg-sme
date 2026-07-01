namespace RecomendationSystem.Services.Forecast;

public sealed class ScenarioLineDto
{
    public int SdgCode { get; init; }
    public ScenarioType Scenario { get; init; }
    public string Label { get; init; } = string.Empty;
    public double StartValue { get; init; }
    public double[] Points { get; init; } = Array.Empty<double>();
}
