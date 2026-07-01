using RecomendationSystem.Domain.Results;
using RecomendationSystem.Models;
using RecomendationSystem.Models.Entities;
using RecomendationSystem.Models.News;

namespace RecomendationSystem.Services.News
{
    public interface IApiNewsService
    {
        Task<OperationResult<List<PestelNewsDto>>> GetApi();

        Task<OperationResult<NewsWithRecommendationsDto>> GetNewsWithRecommendations(int companyId);
        Task<OperationResult<NewsWithRecommendationsDto>> GetNewsWithRecommendations1(List<Sdg> sdgs);
    }
}
