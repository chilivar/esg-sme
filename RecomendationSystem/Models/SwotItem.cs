namespace RecomendationSystem.Models
{
    public class SwotItem
    {
        public int SdgCode { get; set; }

        public string ExternalFactorTitle { get; set; }

        public double InternalValue { get; set; }

        public double ExternalImpact { get; set; }

        public double Weight { get; set; }
    }
}
