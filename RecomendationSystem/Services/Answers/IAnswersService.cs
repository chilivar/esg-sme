using RecomendationSystem.Domain.Results;
using RecomendationSystem.Models;
using RecomendationSystem.Models.Entities;

namespace RecomendationSystem.Services.Answers
{
    public interface IAnswersService
    {
        Task<OperationResult> Memorize(SurveySubmitDto submit);

        Task<OperationResult<List<Sdg>>> GetByCompanyId(int companyId);

        List<Sdg> GetResults(SurveySubmitDto submit);
    }
}