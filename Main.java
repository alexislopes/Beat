import com.pengrad.telegrambot.TelegramBot;
import com.pengrad.telegrambot.TelegramBotAdapter;
import com.pengrad.telegrambot.model.Update;
import com.pengrad.telegrambot.model.request.ChatAction;
import com.pengrad.telegrambot.request.GetUpdates;
import com.pengrad.telegrambot.request.SendChatAction;
import com.pengrad.telegrambot.request.SendMessage;
import com.pengrad.telegrambot.response.BaseResponse;
import com.pengrad.telegrambot.response.GetUpdatesResponse;
import com.pengrad.telegrambot.response.SendResponse;

import java.util.List;

public class Main {

    public static void main(String[] args) {
	    TelegramBot bot = TelegramBotAdapter.build("410547738:AAFuqzUjbIDnDgaXLaEL5AHPPJ6NMJjRSdY");
	    Python python = new Python();
	    Java java = new Java();

        GetUpdatesResponse updatesResponse;
        SendResponse sendResponse;
        BaseResponse baseResponse;
        boolean p=false,j=false;
        int m = 0;

        while(true){

            updatesResponse = bot.execute(new GetUpdates().limit(100).offset(m));

            List<Update> updates = updatesResponse.updates();

            for (Update update: updates) {
                m = update.updateId()+1;

                baseResponse = bot.execute(new SendChatAction(update.message().chat().id(), ChatAction.typing.name()));

                switch (update.message().text().toLowerCase()){



                    case "/start" :
                        sendResponse = bot.execute(new SendMessage(update.message().chat().id(), "Ola, o que voce deseja aprender?"));
                        sendResponse = bot.execute(new SendMessage(update.message().chat().id(), "Java ou Python?"));
                        System.out.println("Recebendo mensagem: " + update.message().text());
                        System.out.println("Resposta de Chat Action enviada? " + baseResponse.isOk());
                        System.out.println("Mensagem enviada?" + sendResponse.isOk());
                    break;


                    case "ola":
                        sendResponse = bot.execute(new SendMessage(update.message().chat().id(), "Ola, como vai você? O que voce deseja aprender?"));
                        System.out.println("Recebendo mensagem: " + update.message().text());
                        System.out.println("Resposta de Chat Action enviada? " + baseResponse.isOk());
                        System.out.println("Mensagem enviada?" + sendResponse.isOk());
                    break;

                    case "python":
                        sendResponse =  bot.execute(new SendMessage(update.message().chat().id(), "Deseja aprender por vídeo ou texto?"));
                        p=true;
                        j=false;
                        System.out.println("Recebendo mensagem: " + update.message().text());
                        System.out.println("Resposta de Chat Action enviada? " + baseResponse.isOk());
                        System.out.println("Mensagem enviada?" + sendResponse.isOk());
                    break;

                    case "java":
                        sendResponse =  bot.execute(new SendMessage(update.message().chat().id(), "Deseja aprender por vídeo ou texto?"));
                        j=true;
                        p=false;
                        System.out.println("Recebendo mensagem: " + update.message().text());
                        System.out.println("Resposta de Chat Action enviada? " + baseResponse.isOk());
                        System.out.println("Mensagem enviada?" + sendResponse.isOk());

                    break;
                    case "video":
                        if(!p && !j) {
                            sendResponse =  bot.execute(new SendMessage(update.message().chat().id(), "Qual matéria voce deseja aprender? Java ou python?"));
                        }
                        else if(p)
                            bot.execute(new SendMessage(update.message().chat().id(),python.videos));
                        else if(j)
                            bot.execute(new SendMessage(update.message().chat().id(),java.videos));
                        break;
                    case "texto":
                        if(!p && !j){
                            sendResponse =  bot.execute(new SendMessage(update.message().chat().id(), "Qual matéria voce deseja aprender? Java ou python?"));
                        }
                        else if(p)
                            bot.execute(new SendMessage(update.message().chat().id(),python.livros));
                        else if(j)
                            bot.execute(new SendMessage(update.message().chat().id(),java.livros));
                        break;
                    default:
                        sendResponse = bot.execute(new SendMessage(update.message().chat().id(), "Não consigo entender isso... ainda!"));
                        System.out.println("Recebendo mensagem: " + update.message().text());
                        System.out.println("Resposta de Chat Action enviada? " + baseResponse.isOk());
                        System.out.println("Mensagem enviada? " + sendResponse.isOk());
                }
            }
        }
    }
}
