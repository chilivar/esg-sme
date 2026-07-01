namespace RecomendationSystem.Models.News
{
    public class NewsWithRecommendationsDto
    {
        public List<PestelNewsDto> News { get; set; } = new();

        public List<SdgRecommendationDto> RecommendedSdgs { get; set; } = new();
    }

    public class SdgRecommendationDto
    {
        public int SdgNumber { get; set; }

        public double CurrentValue { get; set; }

        public double RecommendedValue { get; set; }

        public double Delta { get; set; }
    }
}
