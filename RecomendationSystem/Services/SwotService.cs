using Microsoft.EntityFrameworkCore;
using RecomendationSystem.Constants;
using RecomendationSystem.Data;
using RecomendationSystem.Domain.Results;
using RecomendationSystem.Models;
using RecomendationSystem.Models.Entities;
using RecomendationSystem.Services.News;

namespace RecomendationSystem.Services
{
    public class SwotService : ISwotService
    {
        private readonly IApiNewsService newsService;

        private readonly ApplicationContext context;

        public SwotService(IApiNewsService newsService, ApplicationContext context)
        {
            this.newsService = newsService;
            this.context = context;
        }

        public async Task<OperationResult<SwotResult>> GetSwot(int companyId)
        {
            var sdgs = await context.Sdgs.Where(s => s.CompanyId == companyId).ToListAsync();
            var newsResult = await newsService.GetApi();
            if (!newsResult.IsSuccess)
                return OperationResult<SwotResult>.Fail(ApiMessages.Error);
            var news = newsResult.Data;
            var result = new SwotResult
            {
                SO = new List<SwotItem>(),
                ST = new List<SwotItem>(),
                WO = new List<SwotItem>(),
                WT = new List<SwotItem>()
            };

            foreach (var sdg in sdgs)
            {
                bool isStrength = sdg.Value >= 0.5;
                bool isWeakness = sdg.Value < 0.5;

                // нейтральные пропускаем
                if (!isStrength && !isWeakness)
                    continue;

                foreach (var n in news)
                {
                    // если новость не относится к этому ЦУР — мимо
                    if (!n.Sdg.Contains(sdg.Sdg_number.ToString()))
                        continue;

                    var weight = sdg.Value * n.ImpactStrength;

                    var item = new SwotItem
                    {
                        SdgCode = sdg.Sdg_number,
                        ExternalFactorTitle = n.NewsTitle,
                        InternalValue = sdg.Value,
                        ExternalImpact = n.ImpactStrength,
                        Weight = weight
                    };

                    if (isStrength && n.ImpactType == "OPPORTUNITY")
                        result.SO.Add(item);

                    else if (isStrength && n.ImpactType == "THREAT")
                        result.ST.Add(item);

                    else if (isWeakness && n.ImpactType == "OPPORTUNITY")
                        result.WO.Add(item);

                    else if (isWeakness && n.ImpactType == "THREAT")
                        result.WT.Add(item);
                }
            }

            return OperationResult<SwotResult>.Success(result);
        }

        public async Task<OperationResult<SwotResult>> GetSwot1(List<Sdg> sdgs)
        {
            var newsResult = await newsService.GetApi();
            if (!newsResult.IsSuccess)
                return OperationResult<SwotResult>.Fail(ApiMessages.Error);
            var news = newsResult.Data;
            var result = new SwotResult
            {
                SO = new List<SwotItem>(),
                ST = new List<SwotItem>(),
                WO = new List<SwotItem>(),
                WT = new List<SwotItem>()
            };

            foreach (var sdg in sdgs)
            {
                bool isStrength = sdg.Value >= 0.5;
                bool isWeakness = sdg.Value < 0.5;

                // нейтральные пропускаем
                if (!isStrength && !isWeakness)
                    continue;

                foreach (var n in news)
                {
                    // если новость не относится к этому ЦУР — мимо
                    if (!n.Sdg.Contains(sdg.Sdg_number.ToString()))
                        continue;

                    var weight = sdg.Value * n.ImpactStrength;

                    var item = new SwotItem
                    {
                        SdgCode = sdg.Sdg_number,
                        ExternalFactorTitle = n.NewsTitle,
                        InternalValue = sdg.Value,
                        ExternalImpact = n.ImpactStrength,
                        Weight = weight
                    };

                    if (isStrength && n.ImpactType == "OPPORTUNITY")
                        result.SO.Add(item);

                    else if (isStrength && n.ImpactType == "THREAT")
                        result.ST.Add(item);

                    else if (isWeakness && n.ImpactType == "OPPORTUNITY")
                        result.WO.Add(item);

                    else if (isWeakness && n.ImpactType == "THREAT")
                        result.WT.Add(item);
                }
            }

            return OperationResult<SwotResult>.Success(result);
        }
    }
}