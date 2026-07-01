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
public class ZakonParserService {

    private final String FINANCE_LINK = "https://www.zakon.kz/finansy/";
    private final String POLITIC_LINK = "https://www.zakon.kz/politika/";
    private final String ECOLOGY_LINK = "https://www.zakon.kz/search/?handler=LoadMoreNews&qsearch=%D1%8D%D0%BA%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F&author=0&category=0&tag=0&perioddate=&p=1";
    private final String BASE_URL = "https://www.zakon.kz";

    private final NewsRepository newsRepository;
    private final YandexTranslateService translateService;

    public ZakonParserService(NewsRepository newsRepository,
                              YandexTranslateService translateService) {
        this.newsRepository = newsRepository;
        this.translateService = translateService;
    }

    public void parseFinanceAndSave() throws IOException {
        parseAndSave(FINANCE_LINK);
    }

    public void parsePoliticAndSave() throws IOException {
        parseAndSave(POLITIC_LINK);
    }

    public void parseEcologyAndSave() throws IOException {
        parseAndSave(ECOLOGY_LINK);
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
        Elements cards = doc.select("a.newscard_link");

        List<News> newsList = new ArrayList<>();

        int count = 0;

        for (Element card : cards) {
            if (count >= 10) break;

            String title = card.select(".newscard__title").text().trim();
            String href = card.attr("href").trim();

            if (!title.isEmpty() && !href.isEmpty()) {
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

            news.setSource(SOURCE_ZAKON_KZ);
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