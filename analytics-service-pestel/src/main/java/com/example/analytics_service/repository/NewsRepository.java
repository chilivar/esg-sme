package com.example.analytics_service.repository;

import com.example.analytics_service.model.News;
import org.springframework.data.jpa.repository.JpaRepository;

public interface NewsRepository extends JpaRepository<News, Long> {
}
