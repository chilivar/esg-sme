using Microsoft.AspNetCore.Mvc;
using RecomendationSystem.Services.OpenAiChat;

namespace RecomendationSystem.Controllers
{
    public class OpenAiChatController : BaseController
    {
        private readonly OpenAiChatService _chat;

        public OpenAiChatController(OpenAiChatService chat) => _chat = chat;

        [HttpPost]
        public async Task<IActionResult> Ask(int companyId, string language, CancellationToken ct)
        {
            if(language == "ru" ||  language == "kz" || language == "en")
            {
                var answer = await _chat.AskAsync(companyId, language, ct);
                return Ok(new { answer });
            }
            return BadRequest();
        }
    }
}
