package com.example.analytics_service.repository;

import com.example.analytics_service.model.NewsAnalysisEntity;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface NewsAnalysisRepository extends JpaRepository<NewsAnalysisEntity, Long> {
    Optional<NewsAnalysisEntity> findByNewsId(Long newsId);
}