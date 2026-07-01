package com.example.analytics_service.Controller;

import com.example.analytics_service.dto.NewsImpactResponse;
import com.example.analytics_service.service.NewsImpactService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/news")
public class NewsImpactController {

    private final NewsImpactService service;

    public NewsImpactController(NewsImpactService service) {
        this.service = service;
    }

    @GetMapping("/impacts")
    public List<NewsImpactResponse> getImpacts() {
        return service.getNewsImpacts();
    }

    @GetMapping("/titles")
    public List<String> getTitles() {
        return service.getNews();
    }
}