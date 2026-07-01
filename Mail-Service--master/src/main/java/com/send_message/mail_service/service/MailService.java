package com.send_message.mail_service.service;

import com.send_message.mail_service.dto.MailRequest;
import com.send_message.mail_service.dto.TemplateMailRequest;
import jakarta.mail.MessagingException;
import jakarta.mail.internet.MimeMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Value;

@Service
public class MailService {

    private final JavaMailSender mailSender;

    @Value("${spring.mail.username}")
    private String fromEmail;

    public MailService(JavaMailSender mailSender) {
        this.mailSender = mailSender;
    }

    public void sendMessage(MailRequest request) {
        try {
            for (String recipient : request.getRecipients()) {
                MimeMessage message = mailSender.createMimeMessage();

                MimeMessageHelper helper = new MimeMessageHelper(message, true, "UTF-8");

                helper.setFrom(fromEmail);
                helper.setTo(recipient);
                helper.setSubject(request.getSubject());
                helper.setText(request.getMessage(), true);

                mailSender.send(message);
            }

        } catch (MessagingException e) {
            throw new RuntimeException("Ошибка при отправке письма", e);
        }
    }

    private void sendHtmlEmail(String to, String subject, String htmlMessage) {
        try {
            MimeMessage message = mailSender.createMimeMessage();

            MimeMessageHelper helper = new MimeMessageHelper(message, true, "UTF-8");

            helper.setFrom(fromEmail);
            helper.setTo(to);
            helper.setSubject(subject);
            helper.setText(htmlMessage, true);

            mailSender.send(message);

        } catch (MessagingException e) {
            throw new RuntimeException("Ошибка при отправке письма", e);
        }
    }

    public void sendRegistrationMessage(TemplateMailRequest request) {
        String subject = "Подтверждение регистрации";

        String htmlMessage = buildRegistrationTemplate(
                request.getUsername(),
                request.getLink()
        );

        sendHtmlEmail(request.getEmail(), subject, htmlMessage);
    }

    public void sendPasswordResetMessage(TemplateMailRequest request) {
        String subject = "Сброс пароля";

        String htmlMessage = buildPasswordResetTemplate(
                request.getUsername(),
                request.getLink()
        );

        sendHtmlEmail(request.getEmail(), subject, htmlMessage);
    }

    private String buildRegistrationTemplate(String username, String link) {
        return """
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            background-color: #f4f4f4;
                            padding: 20px;
                        }
                        .container {
                            max-width: 600px;
                            margin: 0 auto;
                            background-color: #ffffff;
                            padding: 30px;
                            border-radius: 10px;
                        }
                        .button {
                            display: inline-block;
                            padding: 12px 20px;
                            background-color: #2563eb;
                            color: #ffffff !important;
                            text-decoration: none;
                            border-radius: 6px;
                            margin-top: 20px;
                        }
                        .footer {
                            margin-top: 30px;
                            font-size: 12px;
                            color: #777777;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h2>Добро пожаловать, %s!</h2>
                        <p>Спасибо за регистрацию.</p>
                        <p>Чтобы подтвердить вашу учетную запись, нажмите на кнопку ниже:</p>
                
                        <a href="%s" class="button">Подтвердить регистрацию</a>
                
                        <p>Если кнопка не работает, скопируйте и откройте ссылку:</p>
                        <p>%s</p>
                
                        <div class="footer">
                            <p>Если вы не регистрировались, просто проигнорируйте это письмо.</p>
                        </div>
                    </div>
                </body>
                </html>
                """.formatted(username, link, link);
    }

    private String buildPasswordResetTemplate(String username, String link) {
        return """
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            background-color: #f4f4f4;
                            padding: 20px;
                        }
                        .container {
                            max-width: 600px;
                            margin: 0 auto;
                            background-color: #ffffff;
                            padding: 30px;
                            border-radius: 10px;
                        }
                        .button {
                            display: inline-block;
                            padding: 12px 20px;
                            background-color: #dc2626;
                            color: #ffffff !important;
                            text-decoration: none;
                            border-radius: 6px;
                            margin-top: 20px;
                        }
                        .footer {
                            margin-top: 30px;
                            font-size: 12px;
                            color: #777777;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h2>Здравствуйте, %s!</h2>
                        <p>Мы получили запрос на сброс пароля.</p>
                        <p>Чтобы создать новый пароль, нажмите на кнопку ниже:</p>
                
                        <a href="%s" class="button">Сбросить пароль</a>
                
                        <p>Если кнопка не работает, скопируйте и откройте ссылку:</p>
                        <p>%s</p>
                
                        <div class="footer">
                            <p>Если вы не запрашивали сброс пароля, просто проигнорируйте это письмо.</p>
                        </div>
                    </div>
                </body>
                </html>
                """.formatted(username, link, link);
    }
}