package com.news_parser_service.demo.controller;

import com.news_parser_service.demo.service.ZakonParserService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/parser/zakon")
public class ZakonParserController {

    private final ZakonParserService parserService;

    public ZakonParserController(ZakonParserService parserService) {
        this.parserService = parserService;
    }

    @GetMapping("/finance")
    public void parseFinance() throws Exception {
        parserService.parseFinanceAndSave();
    }

    @GetMapping("/politic")
    public void parsePolitic() throws Exception {
        parserService.parsePoliticAndSave();
    }

    @GetMapping("/all")
    public void parseAll() throws Exception {
        parserService.parsePoliticAndSave();
        parserService.parseFinanceAndSave();
    }
}
