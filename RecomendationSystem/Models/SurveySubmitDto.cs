using System.Text.Json.Serialization;

namespace RecomendationSystem.Models
{
    public class SurveySubmitDto
    {
        [JsonPropertyName("company_id")]
        public int CompanyId { get; set; }

        [JsonPropertyName("questionnaire_id")]
        public int QuestionnaireId { get; set; }

        [JsonPropertyName("submitted_at")]
        public DateTimeOffset SubmittedAt { get; set; }

        [JsonPropertyName("answers")]
        public List<SurveyAnswerDto> Answers { get; set; } = new();
    }
}
