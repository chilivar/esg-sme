namespace RecomendationSystem.Models
{
    public class PestelNewsDto
    {
        public string NewsTitle { get; set; } = string.Empty;

        public string PestelType { get; set; } = string.Empty;
        // P, E, S, T, E2, L — если захочешь, можно потом заменить на enum

        public string ImpactType { get; set; } = string.Empty;
        // THREAT / OPPORTUNITY и т.п.

        public double ImpactStrength { get; set; }

        public List<string> Sdg { get; set; } = new();

        public string Url { get; set; } = string.Empty;

        public string TitleEn { get; set; } = string.Empty;

        public string TitleKz { get; set; } = string.Empty;
    }
}
