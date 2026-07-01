using Microsoft.EntityFrameworkCore;
using RecomendationSystem.Data;
using RecomendationSystem.Services;
using RecomendationSystem.Services.Answers;
using RecomendationSystem.Services.Forecast;
using RecomendationSystem.Services.News;
using RecomendationSystem.Services.OpenAiChat;
using System.Net.Http.Headers;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddSwaggerGen();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddHttpClient();
builder.Services.AddScoped<IMultiYearForecastService, MultiYearForecastService>();

builder.Services.AddDbContext<ApplicationContext>(options => 
options.UseSqlite(builder.Configuration.GetConnectionString("DefaultConnection")));

builder.Services.AddHttpClient("OpenAI", client =>
{
    client.BaseAddress = new Uri("https://api.openai.com/v1/");
    var key = Environment.GetEnvironmentVariable("AI_KEY")
              ?? throw new InvalidOperationException("OpenAI:ApiKey is missing");
    client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", key);
});

builder.Services.AddScoped<OpenAiChatService>();

builder.Services.AddCors(opt =>
        opt.AddPolicy("CorsPolicy", policy =>
        {
            policy.AllowAnyMethod()
            .AllowAnyHeader()
            .WithOrigins("*");
        }
        ));

builder.Services.AddScoped<IAnswersService, AnswersService>();
builder.Services.AddScoped<IApiNewsService, ApiNewsService>();
builder.Services.AddScoped<ISwotService, SwotService>();
builder.Services.AddScoped<ICategoriesService, CategoriesService>();
var app = builder.Build();

app.UseSwagger();
app.UseSwaggerUI();

app.MapControllers();
app.UseCors("CorsPolicy");

app.Run();
