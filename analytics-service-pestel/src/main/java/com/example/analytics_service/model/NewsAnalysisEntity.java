package com.example.analytics_service.model;

import jakarta.persistence.*;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "news_analysis")
public class NewsAnalysisEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "news_id", nullable = false, unique = true)
    private Long newsId;

    @Column(name = "pestel_type", nullable = false, length = 50)
    private String pestelType;

    @Column(name = "impact_type", nullable = false, length = 50)
    private String impactType;

    @Column(name = "impact_strength", nullable = false, precision = 5, scale = 2)
    private BigDecimal impactStrength;

    @Column(name = "sdg_codes", nullable = false, length = 100)
    private String sdgCodes;

    @Column(name = "analyzed_at", insertable = false, updatable = false)
    private LocalDateTime analyzedAt;

    public Long getId() {
        return id;
    }

    public Long getNewsId() {
        return newsId;
    }

    public void setNewsId(Long newsId) {
        this.newsId = newsId;
    }

    public String getPestelType() {
        return pestelType;
    }

    public void setPestelType(String pestelType) {
        this.pestelType = pestelType;
    }

    public String getImpactType() {
        return impactType;
    }

    public void setImpactType(String impactType) {
        this.impactType = impactType;
    }

    public BigDecimal getImpactStrength() {
        return impactStrength;
    }

    public void setImpactStrength(BigDecimal impactStrength) {
        this.impactStrength = impactStrength;
    }

    public String getSdgCodes() {
        return sdgCodes;
    }

    public void setSdgCodes(String sdgCodes) {
        this.sdgCodes = sdgCodes;
    }

    public LocalDateTime getAnalyzedAt() {
        return analyzedAt;
    }
}