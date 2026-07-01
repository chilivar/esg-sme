package com.example.analytics_service.dto;

import java.math.BigDecimal;
import java.util.List;

public class NewsImpactResponse {

    private String newsTitle;
    private String impactType;
    private BigDecimal impactStrength;
    private List<String> sdg;
    private String pestelType;
    private String titleEn;
    private String titleKz;
    private String url;

    public NewsImpactResponse(String newsTitle,
                              String titleEn,
                              String titleKz,
                              String pestelType,
                              String impactType,
                              BigDecimal impactStrength,
                              List<String> sdg,
                              String url) {
        this.newsTitle = newsTitle;
        this.pestelType = pestelType;
        this.impactType = impactType;
        this.impactStrength = impactStrength;
        this.sdg = sdg;
        this.titleEn = titleEn;
        this.titleKz = titleKz;
        this.url = url;
    }

    public String getNewsTitle() { return newsTitle; }
    public String getImpactType() { return impactType; }
    public BigDecimal getImpactStrength() { return impactStrength; }
    public List<String> getSdg() { return sdg; }
    public String getPestelType() { return pestelType; }
    public String getTitleEn() { return titleEn; }
    public String getTitleKz() { return titleKz; }
    public String getUrl() { return url;}
}
