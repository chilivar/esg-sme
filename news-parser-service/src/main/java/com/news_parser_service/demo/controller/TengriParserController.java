package com.news_parser_service.demo.controller;

import com.news_parser_service.demo.service.TengriParserService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/parser/tengri")
public class TengriParserController {

    private final TengriParserService tengriService;

    public TengriParserController(TengriParserService tengriService) {
        this.tengriService = tengriService;
    }

    @GetMapping("/all")
    public void parseAll() throws Exception {
        tengriService.parseEconomicAndSave();
        tengriService.parseTaxesAndSave();
        tengriService.parseBusinessAndSave();
        tengriService.parseTechAndSave();
    }
}