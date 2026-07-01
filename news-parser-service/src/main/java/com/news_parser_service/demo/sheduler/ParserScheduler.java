package com.news_parser_service.demo.sheduler;

import com.news_parser_service.demo.service.ParserAllSourcesService;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class ParserScheduler {

    private final ParserAllSourcesService parserAllSourcesService;

    public ParserScheduler(ParserAllSourcesService parserAllSourcesService) {
        this.parserAllSourcesService = parserAllSourcesService;
    }

    @Scheduled(cron = "0 0 3 * * MON", zone = "Asia/Almaty")
    public void parseAllWeekly() {
        try {
            parserAllSourcesService.parseAll();
            System.out.println("Weekly parsing completed");
        } catch (Exception e) {
            System.err.println("Error during weekly parsing: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
