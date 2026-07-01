package com.example.analytics_service.service;
import com.example.analytics_service.dto.NewsImpactResponse;
import com.example.analytics_service.model.News;
import com.example.analytics_service.model.NewsAnalysisEntity;
import com.example.analytics_service.model.NewsAnalysisResult;
import com.example.analytics_service.model.NewsAnalyzer;
import com.example.analytics_service.repository.NewsAnalysisRepository;
import com.example.analytics_service.repository.NewsRepository;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;

@Service
public class NewsImpactService {

    private final NewsRepository newsRepository;
    private final NewsAnalysisRepository newsAnalysisRepository;
    private final NewsAnalyzer newsAnalyzer;

    public NewsImpactService(
            NewsRepository newsRepository,
            NewsAnalysisRepository newsAnalysisRepository,
            NewsAnalyzer newsAnalyzer
    ) {
        this.newsRepository = newsRepository;
        this.newsAnalysisRepository = newsAnalysisRepository;
        this.newsAnalyzer = newsAnalyzer;
    }

    public List<String> getNews() {
        return newsRepository.findAll()
                .stream()
                .map(News::getTitle)
                .toList();
    }

    public List<NewsImpactResponse> getNewsImpacts() {
        List<News> allNews = newsRepository.findAll();
        List<NewsAnalysisEntity> allAnalysis = newsAnalysisRepository.findAll();

        Map<Long, NewsAnalysisEntity> analysisByNewsId = allAnalysis.stream()
                .collect(Collectors.toMap(
                        NewsAnalysisEntity::getNewsId,
                        Function.identity(),
                        (a, b) -> a
                ));

        List<News> newsToAnalyze = allNews.stream()
                .filter(news -> !analysisByNewsId.containsKey(news.getId()))
                .toList();

        if (!newsToAnalyze.isEmpty()) {
            List<NewsAnalysisResult> results = newsAnalyzer.analyzeBatch(newsToAnalyze);

            List<NewsAnalysisEntity> newEntities = new ArrayList<>();

            for (int i = 0; i < newsToAnalyze.size(); i++) {
                News news = newsToAnalyze.get(i);
                NewsAnalysisResult result = results.get(i);

                NewsAnalysisEntity entity = new NewsAnalysisEntity();
                entity.setNewsId(news.getId());
                entity.setPestelType(result.getPestelType());
                entity.setImpactType(result.getImpactType());
                entity.setImpactStrength(result.getImpactStrength());
                entity.setSdgCodes(joinSdgCodes(result.getSdgCodes()));

                newEntities.add(entity);
            }

            List<NewsAnalysisEntity> savedEntities = newsAnalysisRepository.saveAll(newEntities);

            for (NewsAnalysisEntity entity : savedEntities) {
                analysisByNewsId.put(entity.getNewsId(), entity);
            }
        }

        List<NewsImpactResponse> responses = allNews.stream()
                .map(news -> {
                    NewsAnalysisEntity entity = analysisByNewsId.get(news.getId());
                    if (entity == null) {
                        return null;
                    }

                    return buildResponse(
                            news,
                            entity.getPestelType(),
                            entity.getImpactType(),
                            entity.getImpactStrength(),
                            parseSdgCodes(entity.getSdgCodes())
                    );
                })
                .filter(Objects::nonNull)
                .toList();

        return filterOneOpportunityAndOneThreatPerPestel(responses);
    }

    private List<NewsImpactResponse> filterOneOpportunityAndOneThreatPerPestel(
            List<NewsImpactResponse> responses
    ) {
        Map<String, NewsImpactResponse> bestByPestelAndImpact = new LinkedHashMap<>();

        for (NewsImpactResponse response : responses) {
            String key = response.getPestelType() + "_" + response.getImpactType();

            NewsImpactResponse current = bestByPestelAndImpact.get(key);

            if (current == null ||
                    response.getImpactStrength().compareTo(current.getImpactStrength()) > 0) {
                bestByPestelAndImpact.put(key, response);
            }
        }

        return new ArrayList<>(bestByPestelAndImpact.values());
    }

    private String joinSdgCodes(List<String> sdgCodes) {
        if (sdgCodes == null || sdgCodes.isEmpty()) {
            return "";
        }
        return String.join(",", sdgCodes);
    }

    private List<String> parseSdgCodes(String sdgCodes) {
        if (sdgCodes == null || sdgCodes.isBlank()) {
            return List.of();
        }

        return Arrays.stream(sdgCodes.split(","))
                .map(String::trim)
                .filter(s -> !s.isEmpty())
                .toList();
    }

    private NewsImpactResponse buildResponse(
            News news,
            String pestelType,
            String impactType,
            BigDecimal impactStrength,
            List<String> sdgCodes
    ) {
        return new NewsImpactResponse(
                news.getTitle(),
                news.getTitleEn(),
                news.getTitleKz(),
                pestelType,
                impactType,
                impactStrength,
                sdgCodes,
                news.getUrl()
        );
    }
}