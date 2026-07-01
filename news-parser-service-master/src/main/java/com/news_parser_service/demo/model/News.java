package com.news_parser_service.demo.model;

import jakarta.persistence.*;
import lombok.Data;

import java.time.LocalDateTime;

@Entity
@Table(name = "news")
@Data
public class News {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String source;
    private String title;
    @Column(name = "title_en")
    private String titleEn;
    @Column(name = "title_kz")
    private String titleKz;
    private String url;
    @Column(name = "published_at")
    private LocalDateTime publishedAt;

    public Long getId() {
        return id;
    }
    public String getSource() {
        return source;
    }
    public String getTitle() {
        return title;
    }
    public String getTitleEn() {
        return titleEn;
    }
    public String getTitleKz() {
        return titleKz;
    }
    public String getUrl() {
        return url;
    }
    public LocalDateTime getPublishedAt() {
        return publishedAt;
    }

    public void setSource(String source) {
        this.source = source;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public void setPublishedAt(LocalDateTime publishedAt) {
        this.publishedAt = publishedAt;
    }

    public void setTitleEn(String titleEn) {
        this.titleEn = titleEn;
    }

    public void setTitleKz(String titleKz) {
        this.titleKz = titleKz;
    }

    public void setUrl(String url) {
        this.url = url;
    }
}
