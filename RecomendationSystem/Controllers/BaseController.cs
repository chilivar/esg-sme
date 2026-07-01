using Microsoft.AspNetCore.Mvc;
using RecomendationSystem.Domain.Results;

namespace RecomendationSystem.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class BaseController : ControllerBase
    {
        protected IActionResult FromResult(OperationResult result)
        {
            return result.IsSuccess ? Ok(result.Message) : BadRequest(result.Message);
        }

        protected IActionResult FromResult<T>(OperationResult<T> result)
        {
            return result.IsSuccess ? Ok(result.Data) : BadRequest(result.Message);
        }
    }
}
