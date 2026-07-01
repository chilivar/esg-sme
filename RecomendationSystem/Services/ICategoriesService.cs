using RecomendationSystem.Models.Entities;

namespace RecomendationSystem.Services
{
    public interface ICategoriesService
    {
        List<Category> GetResults(List<Sdg> sdgs, string language);
    }
}