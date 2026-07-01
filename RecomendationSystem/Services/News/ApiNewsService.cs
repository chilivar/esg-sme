using Microsoft.EntityFrameworkCore;
using RecomendationSystem.Constants;
using RecomendationSystem.Data;
using RecomendationSystem.Domain.Results;
using RecomendationSystem.Models;
using RecomendationSystem.Models.Entities;
using RecomendationSystem.Models.News;

namespace RecomendationSystem.Services.News
{
    public class ApiNewsService : IApiNewsService
    {
        private const double ThreatWeight = 1.0;
        private const double OpportunityWeight = -0.6;
        private const double ImpactScale = 3.0;
        private const double MaxRelativeStep = 0.35;

        private readonly HttpClient httpClient;
        private readonly ApplicationContext context;

        public ApiNewsService(HttpClient httpClient, ApplicationContext context)
        {
            this.httpClient = httpClient;
            this.context = context;
        }

        public async Task<OperationResult<List<PestelNewsDto>>> GetApi()
        {
            var data = await httpClient.GetFromJsonAsync<List<PestelNewsDto>>("http://analytics-service:8083/api/news/impacts");
            //var data = await httpClient.GetFromJsonAsync<List<PestelNewsDto>>("http://localhost:8083/api/news/impacts");
            if (data != null)
                return OperationResult<List<PestelNewsDto>>.Success(data);
            return OperationResult<List<PestelNewsDto>>.Fail(ApiMessages.Error);
        }

        public async Task<OperationResult<NewsWithRecommendationsDto>> GetNewsWithRecommendations(int companyId)
        {
            var newsResult = await GetApi();
            if (!newsResult.IsSuccess || newsResult.Data == null)
                return OperationResult<NewsWithRecommendationsDto>.Fail(newsResult.Message);

            var companySdgs = await context.Sdgs.Where(x => x.CompanyId == companyId).ToListAsync();

            var impactsBySdg = new Dictionary<int, double>();
            foreach (var item in newsResult.Data)
            {
                var impact = item.ImpactStrength * GetImpactWeight(item.ImpactType);
                foreach (var sdgRaw in item.Sdg)
                {
                    if (!int.TryParse(sdgRaw, out var sdgNumber))
                        continue;

                    if (impactsBySdg.ContainsKey(sdgNumber))
                        impactsBySdg[sdgNumber] += impact;
                    else
                        impactsBySdg[sdgNumber] = impact;
                }
            }

            var recommended = impactsBySdg
                .Select(x =>
                {
                    var currentValue = companySdgs.FirstOrDefault(s => s.Sdg_number == x.Key)?.Value ?? 0;
                    if (currentValue == 0)
                        return null;

                    var normalizedPressure = Math.Tanh(x.Value / ImpactScale);
                    var availableRange = normalizedPressure >= 0
                        ? 1 - currentValue
                        : currentValue;
                    var rawDelta = normalizedPressure * MaxRelativeStep * availableRange;
                    var recommendedValue = Math.Clamp(currentValue + rawDelta, 0, 1);
                    var delta = recommendedValue - currentValue;
                    return new SdgRecommendationDto
                    {
                        SdgNumber = x.Key,
                        CurrentValue = Math.Round(currentValue, 2),
                        RecommendedValue = Math.Round(recommendedValue, 2),
                        Delta = Math.Round(delta, 2)
                    };
                })
                .Where(x => x != null)
                .Select(x => x!)
                .OrderBy(x => x.SdgNumber)
                .ToList();

            return OperationResult<NewsWithRecommendationsDto>.Success(new NewsWithRecommendationsDto
            {
                News = newsResult.Data,
                RecommendedSdgs = recommended
            });
        }

        private static double GetImpactWeight(string impactType)
        {
            if (impactType.Equals("THREAT", StringComparison.OrdinalIgnoreCase))
                return ThreatWeight;

            if (impactType.Equals("OPPORTUNITY", StringComparison.OrdinalIgnoreCase))
                return OpportunityWeight;

            return 0;
        }

        public async Task<OperationResult<NewsWithRecommendationsDto>> GetNewsWithRecommendations1(List<Sdg> sdgs)
        {
            var newsResult = await GetApi();
            if (!newsResult.IsSuccess || newsResult.Data == null)
                return OperationResult<NewsWithRecommendationsDto>.Fail(newsResult.Message);

            var companySdgs = sdgs;

            var impactsBySdg = new Dictionary<int, double>();
            foreach (var item in newsResult.Data)
            {
                var impact = item.ImpactStrength * GetImpactWeight(item.ImpactType);
                foreach (var sdgRaw in item.Sdg)
                {
                    if (!int.TryParse(sdgRaw, out var sdgNumber))
                        continue;

                    if (impactsBySdg.ContainsKey(sdgNumber))
                        impactsBySdg[sdgNumber] += impact;
                    else
                        impactsBySdg[sdgNumber] = impact;
                }
            }

            var recommended = impactsBySdg
                .Select(x =>
                {
                    var currentValue = companySdgs.FirstOrDefault(s => s.Sdg_number == x.Key)?.Value ?? 0;
                    if (currentValue == 0)
                        return null;

                    var normalizedPressure = Math.Tanh(x.Value / ImpactScale);
                    var availableRange = normalizedPressure >= 0
                        ? 1 - currentValue
                        : currentValue;
                    var rawDelta = normalizedPressure * MaxRelativeStep * availableRange;
                    var recommendedValue = Math.Clamp(currentValue + rawDelta, 0, 1);
                    var delta = recommendedValue - currentValue;
                    return new SdgRecommendationDto
                    {
                        SdgNumber = x.Key,
                        CurrentValue = Math.Round(currentValue, 2),
                        RecommendedValue = Math.Round(recommendedValue, 2),
                        Delta = Math.Round(delta, 2)
                    };
                })
                .Where(x => x != null)
                .Select(x => x!)
                .OrderBy(x => x.SdgNumber)
                .ToList();

            return OperationResult<NewsWithRecommendationsDto>.Success(new NewsWithRecommendationsDto
            {
                News = newsResult.Data,
                RecommendedSdgs = recommended
            });
        }
    }
}
