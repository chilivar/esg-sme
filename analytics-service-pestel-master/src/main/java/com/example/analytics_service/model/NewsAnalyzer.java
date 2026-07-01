package com.example.analytics_service.model;

import java.util.List;

public interface NewsAnalyzer {
    List<NewsAnalysisResult> analyzeBatch(List<News> newsList);
}
