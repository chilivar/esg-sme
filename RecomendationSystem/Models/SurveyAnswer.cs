namespace RecomendationSystem.Models
{
    using System.Text.Json.Serialization;
    public class SurveyAnswerDto
    {
        [JsonPropertyName("sdg_number")]
        public int SdgNumber { get; set; }

        [JsonPropertyName("weight")]
        public double Weight { get; set; }

        [JsonPropertyName("score")]
        public int Score { get; set; }
    }
}
