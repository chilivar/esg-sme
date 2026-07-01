package com.news_parser_service.demo.repository;

import com.news_parser_service.demo.model.News;
import org.springframework.data.jpa.repository.JpaRepository;

public interface NewsRepository extends JpaRepository<News, Long> {
    boolean existsByTitle(String title);
}
