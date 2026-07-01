using Microsoft.EntityFrameworkCore;
using RecomendationSystem.Constants;
using RecomendationSystem.Data;
using RecomendationSystem.Domain.Results;
using RecomendationSystem.Models;
using RecomendationSystem.Models.Entities;

namespace RecomendationSystem.Services.Answers
{
    public class AnswersService : IAnswersService
    {
        private readonly ApplicationContext context;

        public AnswersService(ApplicationContext context)
        {
            this.context = context;
        }

        public async Task<OperationResult> Memorize(SurveySubmitDto submit)
        {
            var sdgs = Process(submit);
            var contextSdgs = await context.Sdgs.Where(s => s.CompanyId == submit.CompanyId).ToListAsync();
            if (contextSdgs != null)
            {
                context.Sdgs.RemoveRange(contextSdgs);
            }
            await context.Sdgs.AddRangeAsync(sdgs);
            await context.SaveChangesAsync();
            return OperationResult.Success(AnswersMessages.SuccessSave);
        }

        public async Task<OperationResult<List<Sdg>>> GetByCompanyId(int companyId)
        {
            var sdgs = await context.Sdgs.Where(s => s.CompanyId == companyId).ToListAsync();
            if (sdgs.Count != 0)
                return OperationResult<List<Sdg>>.Success(sdgs);
            return OperationResult<List<Sdg>>.Fail(AnswersMessages.FailCompany);
        }

        private List<Sdg> Process(SurveySubmitDto submit)
        {
            var s = new List<Sdg>();
            foreach (var answer in submit.Answers)
            {
                double v = answer.Weight * answer.Score / 5;
                var element = s.Find(x => x.Sdg_number == answer.SdgNumber);
                if (element != null)
                    element.Value += v;
                else
                    s.Add(new Sdg(submit.CompanyId, answer.SdgNumber, v));
            }
            return s;
        }

        public List<Sdg> GetResults(SurveySubmitDto submit)
        {
            var sdgs = Process(submit);
            return sdgs;
        }
    }
}
