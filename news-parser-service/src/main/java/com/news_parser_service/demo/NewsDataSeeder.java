//package com.news_parser_service.demo;
//
//import com.news_parser_service.demo.repository.NewsRepository;
//import com.news_parser_service.demo.service.TengriParserService;
//import com.news_parser_service.demo.service.ZakonParserService;
//import lombok.extern.slf4j.Slf4j;
//import org.springframework.boot.ApplicationArguments;
//import org.springframework.boot.ApplicationRunner;
//import org.springframework.stereotype.Component;
//
//@Slf4j
//@Component
//public class NewsDataSeeder implements ApplicationRunner {
//
//    private final NewsRepository newsRepository;
//    private final ZakonParserService zakonParserService;
//    private final TengriParserService tengriParserService;
//
//    public NewsDataSeeder(NewsRepository newsRepository,
//                          ZakonParserService zakonParserService,
//                          TengriParserService tengriParserService) {
//        this.newsRepository = newsRepository;
//        this.zakonParserService = zakonParserService;
//        this.tengriParserService = tengriParserService;
//    }
//
//    @Override
//    public void run(ApplicationArguments args) {
//        waitForDatabase();
//
//        if (newsRepository.count() > 0) {
//            System.out.println("Новости уже есть в БД, seed пропущен");
//            return;
//        }
//
//        System.out.println("Запуск seed для новостей...");
//
//        seedZakon();
//        seedTengri();
//
//        System.out.println("Seed для новостей завершён");
//    }
//
//    private void waitForDatabase() {
//        int maxAttempts = 12;
//        int attempt = 1;
//        long delayMs = 5000;
//
//        while (attempt <= maxAttempts) {
//            try {
//                newsRepository.count();
//                System.out.println("База данных готова");
//                return;
//            } catch (Exception e) {
//                System.out.println("БД ещё не готова. Попытка " + attempt + "/" + maxAttempts);
//                sleep(delayMs);
//                attempt++;
//            }
//        }
//
//        throw new RuntimeException("База данных не стала доступной за ожидаемое время");
//    }
//
//    private void seedZakon() {
//        try {
//            zakonParserService.parseFinanceAndSave();
//            System.out.println("Zakon finance успешно сохранены");
//        } catch (Exception e) {
//            System.err.println("Ошибка при seed Zakon finance");
//            e.printStackTrace();
//        }
//
//        try {
//            zakonParserService.parsePoliticAndSave();
//            System.out.println("Zakon politic успешно сохранены");
//        } catch (Exception e) {
//            System.err.println("Ошибка при seed Zakon politic");
//            e.printStackTrace();
//        }
//    }
//
//    private void seedTengri() {
//        try {
//            tengriParserService.parseEconomicAndSave();
//            System.out.println("Tengri economic успешно сохранены");
//        } catch (Exception e) {
//            System.err.println("Ошибка при seed Tengri economic");
//            e.printStackTrace();
//        }
//
//        try {
//            tengriParserService.parseEntrepreneursAndSave();
//            System.out.println("Tengri entrepreneurs успешно сохранены");
//        } catch (Exception e) {
//            System.err.println("Ошибка при seed Tengri entrepreneurs");
//            e.printStackTrace();
//        }
//
//        try {
//            tengriParserService.parseTaxesAndSave();
//            System.out.println("Tengri taxes успешно сохранены");
//        } catch (Exception e) {
//            System.err.println("Ошибка при seed Tengri taxes");
//            e.printStackTrace();
//        }
//
//        try {
//            tengriParserService.parseLawAndSave();
//            System.out.println("Tengri law успешно сохранены");
//        } catch (Exception e) {
//            System.err.println("Ошибка при seed Tengri law");
//            e.printStackTrace();
//        }
//
//        try {
//            tengriParserService.parseBusinessAndSave();
//            System.out.println("Tengri business успешно сохранены");
//        } catch (Exception e) {
//            System.err.println("Ошибка при seed Tengri business");
//            e.printStackTrace();
//        }
//
//        try {
//            tengriParserService.parseTechAndSave();
//            System.out.println("Tengri tech успешно сохранены");
//        } catch (Exception e) {
//            System.err.println("Ошибка при seed Tengri tech");
//            e.printStackTrace();
//        }
//    }
//
//    private void sleep(long delayMs) {
//        try {
//            Thread.sleep(delayMs);
//        } catch (InterruptedException e) {
//            Thread.currentThread().interrupt();
//            throw new RuntimeException("Ожидание БД было прервано", e);
//        }
//    }
//}