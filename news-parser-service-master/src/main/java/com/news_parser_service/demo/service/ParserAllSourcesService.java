package com.news_parser_service.demo.service;

import org.springframework.stereotype.Service;

@Service
public class ParserAllSourcesService {

    private final TengriParserService tengriService;
    private final ZakonParserService zakonService;

    public ParserAllSourcesService(TengriParserService tengriService,
                                   ZakonParserService zakonService) {
        this.tengriService = tengriService;
        this.zakonService = zakonService;
    }

    public void parseAll() throws Exception {
        tengriService.parseEconomicAndSave();
        tengriService.parseTaxesAndSave();
        tengriService.parseBusinessAndSave();
        tengriService.parseTechAndSave();

        zakonService.parsePoliticAndSave();
        zakonService.parseFinanceAndSave();
        zakonService.parseEcologyAndSave();
    }
}
