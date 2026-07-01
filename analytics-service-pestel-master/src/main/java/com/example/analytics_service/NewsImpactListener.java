package com.example.analytics_service;

import com.example.analytics_service.service.NewsImpactService;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;

@Component
public class NewsImpactListener {

    private final NewsImpactService service;

    public NewsImpactListener(NewsImpactService service) {
        this.service = service;
    }

    @RabbitListener(queues = RabbitConfig.QUEUE)
    public void handleMessage(String message) {
        System.out.println("Received: " + message);
        service.getNewsImpacts();
    }
}
