import logging
import requests
import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")
WA_NUMBER = os.getenv("WA_NUMBER")
CALLMEBOT_KEY = os.getenv("CALLMEBOT_KEY")

(NOME, OBJETIVO, QUANTO, TENTOU,
 DISPONIBILIDADE, BUDGET, CONTATO, HORARIO) = range(8)


def send_whatsapp(msg: str):
    """Envia mensagem pro WhatsApp do Leonardo via Callmebot."""
    url = (
        f"https://api.callmebot.com/whatsapp.php"
        f"?phone={WA_NUMBER}"
        f"&text={requests.utils.quote(msg)}"
        f"&apikey={CALLMEBOT_KEY}"
    )
    try:
        response = requests.get(url, timeout=10)
        logger.info(f"Callmebot status: {response.status_code}")
    except Exception as e:
        logger.error(f"Erro ao enviar WhatsApp: {e}")


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data.clear()
    await update.message.reply_text(
        "Oi! ð Sou o assistente da *Carletti Online Coaching*.\n\n"
        "Vou te fazer algumas perguntas rÃ¡pidas pra entender "
        "como posso te ajudar a transformar o seu corpo. ðª\n\n"
        "Qual Ã© o seu *nome completo*?",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove(),
    )
    return NOME


async def nome(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["nome"] = update.message.text.strip()
    kb = [
        ["ð¥ Emagrecer", "ðª Ganhar massa"],
        ["â¤ï¸ SaÃºde geral", "ð Emagrecer e ganhar massa"],
    ]
    await update.message.reply_text(
        f"Prazer, {ctx.user_data['nome']}! ð\n\n"
        "Qual Ã© o seu *objetivo principal* agora?",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(kb, one_time_keyboard=True, resize_keyboard=True),
    )
    return OBJETIVO


async def objetivo(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    obj = update.message.text.strip()
    ctx.user_data["objetivo"] = obj

    if "Ganhar massa" in obj or "SaÃºde geral" in obj:
        await update.message.reply_text(
            "Obrigado por responder! ð\n\n"
            "No momento minha consultoria Ã© focada em *emagrecimento e recomposiÃ§Ã£o corporal*.\n\n"
            "Mas nÃ£o para por aqui! Sigo postando dicas gratuitas no Instagram:\n"
            "ð @leleocarletti\n\n"
            "Quando o seu foco mudar pra emagrecimento, pode me chamar de volta! ðª",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END

    kb = [
        ["Menos de 5kg", "Entre 5 e 15kg"],
        ["Mais de 15kg", "Mais de 30kg"],
    ]
    await update.message.reply_text(
        "Boa escolha! Foco total em resultados. ð¥\n\n"
        "Quanto vocÃª quer emagrecer *aproximadamente*?",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(kb, one_time_keyboard=True, resize_keyboard=True),
    )
    return QUANTO


async def quanto(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["quanto"] = update.message.text.strip()
    kb = [
        ["Sim, vÃ¡rias vezes mas nÃ£o consegui manter"],
        ["Sim, perdi peso mas voltou tudo"],
        ["Nunca tentei com mÃ©todo sÃ©rio"],
    ]
    await update.message.reply_text(
        "Entendido! Agora me conta...\n\n"
        "VocÃª jÃ¡ tentou emagrecer antes com dieta ou treino?",
        reply_markup=ReplyKeyboardMarkup(kb, one_time_keyboard=True, resize_keyboard=True),
    )
    return TENTOU


async def tentou(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["tentou"] = update.message.text.strip()
    kb = [
        ["1 a 2x por semana", "3 a 4x por semana"],
        ["5x ou mais por semana", "Ainda nÃ£o treino"],
    ]
    await update.message.reply_text(
        "Boa! Quantas vezes por semana vocÃª *consegue treinar* atualmente?",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(kb, one_time_keyboard=True, resize_keyboard=True),
    )
    return DISPONIBILIDADE


async def disponibilidade(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["disponibilidade"] = update.message.text.strip()
    kb = [
        ["AtÃ© R$200 por mÃªs", "R$200 a R$500 por mÃªs"],
        ["R$500 a R$1.000 por mÃªs", "Acima de R$1.000 por mÃªs"],
    ]
    await update.message.reply_text(
        "Ãltima pergunta, prometo! ð\n\n"
        "Quanto vocÃª estaria disposto(a) a *investir mensalmente* "
        "na sua transformaÃ§Ã£o corporal?",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(kb, one_time_keyboard=True, resize_keyboard=True),
    )
    return BUDGET


async def budget(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    bud = update.message.text.strip()
    ctx.user_data["budget"] = bud

    if "AtÃ© R$200" in bud:
        await update.message.reply_text(
            "Obrigado pela honestidade! ð\n\n"
            "No momento nÃ£o tenho um plano nessa faixa de investimento, "
            "mas continuo postando muito conteÃºdo gratuito!\n\n"
            "Me segue lÃ¡: ð @leleocarletti no Instagram ð²\n\n"
            "Quando tiver pronto para investir de verdade na sua transformaÃ§Ã£o, "
            "pode voltar aqui! ðª",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END

    await update.message.reply_text(
        "Perfeito! VocÃª estÃ¡ pronto(a) para mudar de vida. ð\n\n"
        "Me passa o seu *nÃºmero de WhatsApp com DDD* "
        "para o Leonardo entrar em contato:\n\n"
        "Ex: 11999999999",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove(),
    )
    return CONTATO


async def contato(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["contato"] = update.message.text.strip()
    kb = [
        ["ManhÃ£ â 8h Ã s 12h", "Tarde â 12h Ã s 18h"],
        ["Noite â 18h Ã s 22h", "Qualquer horÃ¡rio"],
    ]
    await update.message.reply_text(
        "Ãtimo! Qual o *melhor horÃ¡rio* para o Leonardo te ligar?",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(kb, one_time_keyboard=True, resize_keyboard=True),
    )
    return HORARIO


async def horario(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["horario"] = update.message.text.strip()
    d = ctx.user_data

    # Monta mensagem do lead qualificado
    msg = (
        f"ð¥ NOVO LEAD QUALIFICADO â CARLETTI COACHING\n\n"
        f"ð¤ Nome: {d['nome']}\n"
        f"ð¯ Objetivo: {d['objetivo']}\n"
        f"âï¸ Meta de emagrecimento: {d['quanto']}\n"
        f"ð HistÃ³rico: {d['tentou']}\n"
        f"ðï¸ Disponibilidade de treino: {d['disponibilidade']}\n"
        f"ð° Budget mensal: {d['budget']}\n"
        f"ð± WhatsApp: {d['contato']}\n"
        f"ð Melhor horÃ¡rio para contato: {d['horario']}\n\n"
        f"â¡ Lead veio do bot de qualificaÃ§Ã£o no Telegram."
    )

    send_whatsapp(msg)
    logger.info(f"Lead qualificado enviado: {d['nome']} | {d['contato']}")

    await update.message.reply_text(
        f"IncrÃ­vel, {d['nome']}! â\n\n"
        "Suas informaÃ§Ãµes foram enviadas para o Leonardo.\n"
        "Ele vai entrar em contato com vocÃª pelo WhatsApp em breve! ð²\n\n"
        "Enquanto isso, jÃ¡ vai se inspirando:\n"
        "ð @leleocarletti no Instagram ð",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


async def cancelar(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Tudo bem! Se mudar de ideia Ã© sÃ³ mandar /start ð",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


async def erro_handler(update: object, ctx: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Erro no bot: {ctx.error}")


def main():
    if not TOKEN:
        raise ValueError("TELEGRAM_TOKEN nÃ£o definido nas variÃ¡veis de ambiente!")

    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, nome)],
            OBJETIVO: [MessageHandler(filters.TEXT & ~filters.COMMAND, objetivo)],
            QUANTO: [MessageHandler(filters.TEXT & ~filters.COMMAND, quanto)],
            TENTOU: [MessageHandler(filters.TEXT & ~filters.COMMAND, tentou)],
            DISPONIBILIDADE: [MessageHandler(filters.TEXT & ~filters.COMMAND, disponibilidade)],
            BUDGET: [MessageHandler(filters.TEXT & ~filters.COMMAND, budget)],
            CONTATO: [MessageHandler(filters.TEXT & ~filters.COMMAND, contato)],
            HORARIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, horario)],
        },
        fallbacks=[CommandHandler("cancelar", cancelar)],
        allow_reentry=True,
    )

    app.add_handler(conv_handler)
    app.add_error_handler(erro_handler)

    logger.info("Bot Carletti Coaching rodando...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
