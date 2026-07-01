package com.example.analytics_service.service;

import com.example.analytics_service.RabbitConfig;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.stereotype.Service;

@Service
public class NewsImpactPublisher {

    private final RabbitTemplate rabbitTemplate;

    public NewsImpactPublisher(RabbitTemplate rabbitTemplate) {
        this.rabbitTemplate = rabbitTemplate;
    }

    public void sendAnalysisRequest() {
        rabbitTemplate.convertAndSend(
                RabbitConfig.EXCHANGE,
                RabbitConfig.ROUTING_KEY,
                "RUN_NEWS_ANALYSIS"
        );
    }
}
