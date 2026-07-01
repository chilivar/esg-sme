using RecomendationSystem.Domain.Results;
using RecomendationSystem.Models;
using RecomendationSystem.Models.Entities;

namespace RecomendationSystem.Services
{
    public interface ISwotService
    {
        Task<OperationResult<SwotResult>> GetSwot(int companyId);
        Task<OperationResult<SwotResult>> GetSwot1(List<Sdg> sdgs);
    }
}