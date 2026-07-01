package com.example.analytics_service;

import org.springframework.amqp.core.Binding;
import org.springframework.amqp.core.BindingBuilder;
import org.springframework.amqp.core.DirectExchange;
import org.springframework.amqp.core.Queue;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class RabbitConfig {

    public static final String EXCHANGE = "news.analysis.exchange";
    public static final String QUEUE = "news.analysis.queue";
    public static final String ROUTING_KEY = "news.analysis.requested";

    @Bean
    public DirectExchange newsExchange() {
        return new DirectExchange(EXCHANGE);
    }

    @Bean
    public Queue newsQueue() {
        return new Queue(QUEUE, true);
    }

    @Bean
    public Binding binding(Queue newsQueue, DirectExchange newsExchange) {
        return BindingBuilder.bind(newsQueue).to(newsExchange).with(ROUTING_KEY);
    }
}
