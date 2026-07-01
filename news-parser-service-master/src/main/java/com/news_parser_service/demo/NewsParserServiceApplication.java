package com.news_parser_service.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@EnableScheduling
@SpringBootApplication
public class NewsParserServiceApplication {

	public static void main(String[] args) {
		SpringApplication.run(NewsParserServiceApplication.class, args);
		System.out.print("VERSION 1");
	}
}
