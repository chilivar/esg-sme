FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY . .
RUN dotnet restore
RUN dotnet publish -c Release -o /app/publish --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app

# Скопируем опубликованное приложение
COPY --from=build /app/publish .

# Если ты “запекаешь” app.db внутрь publish (вариант А),
# то файл уже попадёт в /app/app.db на строке выше.
# Теперь дадим права пользователю app на /app (и на db тоже).
RUN chown -R app:app /app

USER app
ENV ASPNETCORE_URLS=http://+:5000
EXPOSE 5000
ENTRYPOINT ["dotnet", "RecomendationSystem.dll"]