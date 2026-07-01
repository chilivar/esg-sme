package com.example.analytics_service.model;

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
    @Column(name = "published_at")
    private LocalDateTime publishedAt;
    private String url;

    public String getUrl() {
        return url;
    }

    public Long getId() {
        return id;
    }

    public String getSource() {
        return source;
    }

    public String getTitle() {
        return title;
    }

    public LocalDateTime getPublishedAt() {
        return publishedAt;
    }

    public String getTitleEn() {
        return titleEn;
    }

    public String getTitleKz() {
        return titleKz;
    }
}
