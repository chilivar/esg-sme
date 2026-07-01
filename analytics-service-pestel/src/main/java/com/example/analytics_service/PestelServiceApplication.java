package com.example.analytics_service;

import org.springframework.amqp.rabbit.annotation.EnableRabbit;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@EnableRabbit
@SpringBootApplication
public class PestelServiceApplication {

	public static void main(String[] args) {
		SpringApplication.run(PestelServiceApplication.class, args);
	}
}
