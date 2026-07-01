package com.example.analytics_service.model;

import java.math.BigDecimal;
import java.util.List;

public class NewsAnalysisResult {

    private final String pestelType;
    private final String impactType;
    private final BigDecimal impactStrength;
    private final List<String> sdgCodes;

    public NewsAnalysisResult(
            String pestelType,
            String impactType,
            BigDecimal impactStrength,
            List<String> sdgCodes
    ) {
        this.pestelType = pestelType;
        this.impactType = impactType;
        this.impactStrength = impactStrength;
        this.sdgCodes = sdgCodes;
    }

    public String getPestelType() {
        return pestelType;
    }

    public String getImpactType() {
        return impactType;
    }

    public BigDecimal getImpactStrength() {
        return impactStrength;
    }

    public List<String> getSdgCodes() {
        return sdgCodes;
    }
}