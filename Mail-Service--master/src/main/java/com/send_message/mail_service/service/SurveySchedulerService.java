package com.send_message.mail_service.service;

import com.send_message.mail_service.dto.MailRequest;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class SurveySchedulerService {

    private final MailService mailService;
    private final MailingUserClient mailingUserClient;

    public SurveySchedulerService(MailService mailService, MailingUserClient mailingUserClient) {
        this.mailService = mailService;
        this.mailingUserClient = mailingUserClient;
    }

    @Scheduled(cron = "0 0 10 1 * *")
    public void sendSurveyMailEveryMonth() {
        sendSurveyMail();
    }

    public void sendSurveyMail() {
        List<String> recipients = mailingUserClient.getMailingUsers();

        if (recipients.isEmpty()) {
            return;
        }

        MailRequest request = new MailRequest();
        request.setRecipients(recipients);
        request.setSubject("Пройдите ежемесячный опрос — Портал ЦУР");
        request.setMessage(buildSurveyEmailHtml());

        mailService.sendMessage(request);
    }

    private String buildSurveyEmailHtml() {
        return """
                <!DOCTYPE html>
                <html lang="ru">
                <head>
                    <meta charset="UTF-8">
                    <title>Портал ЦУР</title>
                </head>
                <body style="margin:0; padding:0; background-color:#f4f6f8; font-family:Arial, sans-serif;">
                    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f6f8; padding:30px 0;">
                        <tr>
                            <td align="center">
                                <table width="600" cellpadding="0" cellspacing="0" style="background-color:#ffffff; border-radius:14px; overflow:hidden; box-shadow:0 4px 14px rgba(0,0,0,0.08);">
                                    <tr>
                                        <td style="background-color:#0b5ed7; padding:28px; text-align:center;">
                                            <h1 style="margin:0; color:#ffffff; font-size:26px;">
                                                Портал ЦУР
                                            </h1>
                                        </td>
                                    </tr>

                                    <tr>
                                        <td style="padding:35px 40px;">
                                            <h2 style="margin:0 0 18px; color:#222222; font-size:24px;">
                                                Пройдите ежемесячный опрос
                                            </h2>

                                            <p style="margin:0 0 16px; color:#444444; font-size:16px; line-height:1.6;">
                                                Здравствуйте!
                                            </p>

                                            <p style="margin:0 0 16px; color:#444444; font-size:16px; line-height:1.6;">
                                                Просим вас пройти небольшой опрос на портале ЦУР.
                                            </p>

                                            <p style="margin:0 0 28px; color:#444444; font-size:16px; line-height:1.6;">
                                                Опрос займет всего несколько минут.
                                            </p>

                                            <table cellpadding="0" cellspacing="0" style="margin:0 auto;">
                                                <tr>
                                                    <td align="center" style="background-color:#0b5ed7; border-radius:8px;">
                                                        <a href="https://portal-cur.kz/survey"
                                                           style="display:inline-block; padding:14px 28px; color:#ffffff; text-decoration:none; font-size:16px; font-weight:bold;">
                                                            Пройти опрос
                                                        </a>
                                                    </td>
                                                </tr>
                                            </table>

                                            <p style="margin:30px 0 0; color:#777777; font-size:14px; line-height:1.5;">
                                                Если кнопка не открывается, скопируйте ссылку в браузер:
                                                <br>
                                                <a href="https://portal-cur.kz/survey" style="color:#0b5ed7;">
                                                    https://portal-cur.kz/survey
                                                </a>
                                            </p>
                                        </td>
                                    </tr>

                                    <tr>
                                        <td style="background-color:#f1f3f5; padding:22px 35px; text-align:center;">
                                            <p style="margin:0; color:#666666; font-size:13px; line-height:1.5;">
                                                Это автоматическое письмо от сервиса «Портал ЦУР».
                                                <br>
                                                Пожалуйста, не отвечайте на него.
                                            </p>
                                            <p style="margin:12px 0 0; color:#999999; font-size:12px;">
                                                © 2026 Портал ЦУР
                                            </p>
                                        </td>
                                    </tr>

                                </table>
                            </td>
                        </tr>
                    </table>
                </body>
                </html>
                """;
    }
}