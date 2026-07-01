package com.news_parser_service.demo.service;

import com.news_parser_service.demo.model.News;
import com.news_parser_service.demo.repository.NewsRepository;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

import static com.news_parser_service.demo.constants.SettingsZakonConstants.*;

@Service
public class TengriParserService {

    private final String ECONOMIC_LINK = "https://tengrinews.kz/economic/";
    private final String TAXES_LINK = "https://tengrinews.kz/tag/%D0%BD%D0%B0%D0%BB%D0%BE%D0%B3%D0%B8/";
    private final String BUSINESS_LINK = "https://tengrinews.kz/tag/%D0%B1%D0%B8%D0%B7%D0%BD%D0%B5%D1%81/";
    private final String TECH_LINK = "https://tengrinews.kz/tech/";
    private final String BASE_URL = "https://tengrinews.kz";

    private final NewsRepository newsRepository;
    private final YandexTranslateService translateService;

    public TengriParserService(NewsRepository newsRepository,
                               YandexTranslateService translateService) {
        this.newsRepository = newsRepository;
        this.translateService = translateService;
    }

    public void parseEconomicAndSave() throws IOException {
        parseAndSave(ECONOMIC_LINK);
    }

    public void parseTaxesAndSave() throws IOException {
        parseAndSave(TAXES_LINK);
    }

    public void parseBusinessAndSave() throws IOException {
        parseAndSave(BUSINESS_LINK);
    }

    public void parseTechAndSave() throws IOException {
        parseAndSave(TECH_LINK);
    }

    public void parseAndSave(String url) throws IOException {
        Document doc = loadDocument(url);
        List<News> parsedNews = extractNews(doc);
        List<News> uniqueNews = filterNewNews(parsedNews);
        saveNews(uniqueNews);
    }

    private Document loadDocument(String url) throws IOException {
        return Jsoup.connect(url)
                .userAgent(USER_AGENT)
                .referrer(REFERRER)
                .timeout(TIMEOUT_MS)
                .get();
    }

    private List<News> extractNews(Document doc) {
        Elements cards = doc.select("div.content_main_item");

        List<News> newsList = new ArrayList<>();
        int count = 0;

        for (Element card : cards) {
            if (count >= 10) break;

            Element titleLink = card.selectFirst("span.content_main_item_title a");
            if (titleLink == null) {
                continue;
            }

            String title = titleLink.text().trim();
            String href = titleLink.attr("href").trim();

            if (title.isEmpty() || href.isEmpty()) {
                continue;
            }

            News news = new News();
            news.setTitle(title);

            if (href.startsWith("http")) {
                news.setUrl(href);
            } else {
                news.setUrl(BASE_URL + href);
            }

            newsList.add(news);
            count++;
        }

        return newsList;
    }

    private List<News> filterNewNews(List<News> newsList) {
        List<News> result = new ArrayList<>();

        for (News news : newsList) {
            if (!newsRepository.existsByTitle(news.getTitle())) {
                result.add(news);
            }
        }

        return result;
    }

    private void saveNews(List<News> newsList) {
        if (newsList.isEmpty()) return;

        List<String> titles = newsList.stream()
                .map(News::getTitle)
                .toList();

        List<String> titlesEn = translateService.translateBatch(titles, "en");
        List<String> titlesKz = translateService.translateBatch(titles, "kk");

        for (int i = 0; i < newsList.size(); i++) {
            News news = newsList.get(i);

            news.setSource(SOURCE_TENGRI_KZ);
            news.setPublishedAt(LocalDateTime.now());

            if (i < titlesEn.size()) {
                news.setTitleEn(titlesEn.get(i));
            }

            if (i < titlesKz.size()) {
                news.setTitleKz(titlesKz.get(i));
            }

            newsRepository.save(news);
        }
    }
}