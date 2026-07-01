using RecomendationSystem.Models;

namespace RecomendationSystem.Services.Forecast;

public sealed class MultiYearForecastService : IMultiYearForecastService
{
    public MultiYearForecastChartDto BuildMultiYearForecast(SwotResult swotResult, MultiYearForecastOptions? options = null)
    {
        if (swotResult is null)
        {
            throw new ArgumentNullException(nameof(swotResult));
        }

        options ??= new MultiYearForecastOptions();

        if (options.Years < 1 || options.Years > 10)
        {
            throw new ArgumentOutOfRangeException(nameof(options.Years), "Years should be between 1 and 10.");
        }

        var threatItems = swotResult.WT.Concat(swotResult.ST).ToList();
        if (threatItems.Count == 0)
        {
            return new MultiYearForecastChartDto
            {
                Labels = BuildYearLabels(options.StartYear, options.Years),
                Series = new List<ScenarioLineDto>()
            };
        }

        var sdgPriority = threatItems
            .GroupBy(x => x.SdgCode)
            .Select(g => new
            {
                Sdg = g.Key,
                Score = g.Sum(i => i.Weight),
                Start = g.Average(i => i.InternalValue),
                ThreatImpact = g.Average(i => i.ExternalImpact)
            })
            .OrderByDescending(x => x.Score)
            .Take(Math.Max(1, options.TopSdgCount))
            .ToList();

        var chart = new MultiYearForecastChartDto
        {
            Labels = BuildYearLabels(options.StartYear, options.Years)
        };

        foreach (var item in sdgPriority)
        {
            var start = Clamp01(item.Start);

            chart.Series.Add(BuildLine(item.Sdg, ScenarioType.Base, start, item.ThreatImpact, options));
            chart.Series.Add(BuildLine(item.Sdg, ScenarioType.Optimistic, start, item.ThreatImpact, options));
            chart.Series.Add(BuildLine(item.Sdg, ScenarioType.Negative, start, item.ThreatImpact, options));
        }

        return chart;
    }

    private static ScenarioLineDto BuildLine(int sdg, ScenarioType scenario, double startValue, double threatImpact, MultiYearForecastOptions options)
    {
        var points = new double[options.Years];

        var k = scenario switch
        {
            ScenarioType.Base => options.BaseK,
            ScenarioType.Optimistic => options.OptimisticK,
            ScenarioType.Negative => options.NegativeK,
            _ => options.BaseK
        };

        var actionYear1 = 0.0;
        if (scenario == ScenarioType.Optimistic)
        {
            actionYear1 = options.ActionDeltaBySdg.TryGetValue(sdg, out var delta)
                ? delta
                : options.DefaultActionDelta;
        }

        var current = startValue;

        for (int yearIndex = 0; yearIndex < options.Years; yearIndex++)
        {
            var actionDelta = actionYear1 * Math.Pow(options.ActionDecay, yearIndex);
            var threatDelta = (threatImpact * options.ThreatSensitivity) * Math.Pow(options.ThreatGrowth, yearIndex);

            var next = current + (actionDelta - threatDelta) * k;
            next = Clamp01(next);

            points[yearIndex] = next;
            current = next;
        }

        return new ScenarioLineDto
        {
            SdgCode = sdg,
            Scenario = scenario,
            Label = $"SDG {sdg} - {scenario}",
            StartValue = startValue,
            Points = points
        };
    }

    private static string[] BuildYearLabels(int startYear, int years)
    {
        var labels = new string[years];
        for (var i = 0; i < years; i++)
        {
            labels[i] = (startYear + i + 1).ToString();
        }

        return labels;
    }

    private static double Clamp01(double value)
    {
        if (value < 0)
        {
            return 0;
        }

        if (value > 1)
        {
            return 1;
        }

        return value;
    }
}
