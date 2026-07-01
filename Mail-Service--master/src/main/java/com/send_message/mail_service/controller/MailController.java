package com.send_message.mail_service.controller;

import com.send_message.mail_service.dto.MailRequest;
import com.send_message.mail_service.dto.TemplateMailRequest;
import com.send_message.mail_service.service.MailService;
import com.send_message.mail_service.service.SurveySchedulerService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/messages")
public class MailController {

    private final MailService mailService;
    private final SurveySchedulerService surveySchedulerService;

    public MailController(MailService mailService, SurveySchedulerService surveySchedulerService) {
        this.mailService = mailService;
        this.surveySchedulerService = surveySchedulerService;
    }

    @PostMapping("/send")
    public ResponseEntity<String> sendMessage(@RequestBody MailRequest request) {
        mailService.sendMessage(request);
        return ResponseEntity.ok("Сообщения успешно отправлены");
    }

    @PostMapping("/send-survey")
    public ResponseEntity<String> sendSurveyMail() {
        surveySchedulerService.sendSurveyMail();
        return ResponseEntity.ok("Рассылка опроса успешно запущена");
    }

    @PostMapping("/registration")
    public ResponseEntity<String> sendRegistrationMessage(
            @RequestBody TemplateMailRequest request
    ) {
        mailService.sendRegistrationMessage(request);
        return ResponseEntity.ok("Письмо для регистрации успешно отправлено");
    }

    @PostMapping("/password-reset")
    public ResponseEntity<String> sendPasswordResetMessage(
            @RequestBody TemplateMailRequest request
    ) {
        mailService.sendPasswordResetMessage(request);
        return ResponseEntity.ok("Письмо для сброса пароля успешно отправлено");
    }
}