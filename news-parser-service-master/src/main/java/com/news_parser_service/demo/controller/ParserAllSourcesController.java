package com.news_parser_service.demo.controller;

import com.news_parser_service.demo.service.ParserAllSourcesService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/parser/sources")
public class ParserAllSourcesController {

    private final ParserAllSourcesService parserAllSourcesService;

    public ParserAllSourcesController(ParserAllSourcesService parserAllSourcesService) {
        this.parserAllSourcesService = parserAllSourcesService;
    }

    @GetMapping("/all")
    public String parseAll() throws Exception {
        parserAllSourcesService.parseAll();
        return "All parsing completed";
    }
}
