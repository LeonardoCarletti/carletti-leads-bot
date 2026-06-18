import logging
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
OWNER_CHAT_ID = 5729823175  # Telegram ID do Leonardo

(NOME, OBJETIVO, QUANTO, TENTOU,
 DISPONIBILIDADE, BUDGET, CONTATO, HORARIO) = range(8)


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data.clear()
    await update.message.reply_text(
        "Oi! 👋 Sou o assistente da *Carletti Online Coaching*.\n\n"
        "Vou te fazer algumas perguntas rápidas pra entender "
        "como posso te ajudar a transformar o seu corpo. 💪\n\n"
        "Qual é o seu *nome completo*?",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove(),
    )
    return NOME


async def nome(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["nome"] = update.message.text.strip()
    kb = [
        ["🔥 Emagrecer", "💪 Ganhar massa"],
        ["❤️ Saúde geral", "🔄 Emagrecer e ganhar massa"],
    ]
    await update.message.reply_text(
        f"Prazer, {ctx.user_data['nome']}! 😊\n\n"
        "Qual é o seu *objetivo principal* agora?",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(kb, one_time_keyboard=True, resize_keyboard=True),
    )
    return OBJETIVO


async def objetivo(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    obj = update.message.text.strip()
    ctx.user_data["objetivo"] = obj

    if "Ganhar massa" in obj or "Saúde geral" in obj:
        await update.message.reply_text(
            "Obrigado por responder! 🙏\n\n"
            "No momento minha consultoria é focada em *emagrecimento e recomposição corporal*.\n\n"
            "Mas não para por aqui! Sigo postando dicas gratuitas no Instagram:\n"
            "👉 @leleocarletti\n\n"
            "Quando o seu foco mudar pra emagrecimento, pode me chamar de volta! 💪",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END

    kb = [
        ["Menos de 5kg", "Entre 5 e 15kg"],
        ["Mais de 15kg", "Mais de 30kg"],
    ]
    await update.message.reply_text(
        "Boa escolha! Foco total em resultados. 🔥\n\n"
        "Quanto você quer emagrecer *aproximadamente*?",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(kb, one_time_keyboard=True, resize_keyboard=True),
    )
    return QUANTO


async def quanto(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["quanto"] = update.message.text.strip()
    kb = [
        ["Sim, várias vezes mas não consegui manter"],
        ["Sim, perdi peso mas voltou tudo"],
        ["Nunca tentei com método sério"],
    ]
    await update.message.reply_text(
        "Entendido! Agora me conta...\n\n"
        "Você já tentou emagrecer antes com dieta ou treino?",
        reply_markup=ReplyKeyboardMarkup(kb, one_time_keyboard=True, resize_keyboard=True),
    )
    return TENTOU


async def tentou(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["tentou"] = update.message.text.strip()
    kb = [
        ["1 a 2x por semana", "3 a 4x por semana"],
        ["5x ou mais por semana", "Ainda não treino"],
    ]
    await update.message.reply_text(
        "Boa! Quantas vezes por semana você *consegue treinar* atualmente?",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(kb, one_time_keyboard=True, resize_keyboard=True),
    )
    return DISPONIBILIDADE


async def disponibilidade(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["disponibilidade"] = update.message.text.strip()
    kb = [
        ["Até R$200 por mês", "R$200 a R$500 por mês"],
        ["R$500 a R$1.000 por mês", "Acima de R$1.000 por mês"],
    ]
    await update.message.reply_text(
        "Última pergunta, prometo! 😄\n\n"
        "Quanto você estaria disposto(a) a *investir mensalmente* "
        "na sua transformação corporal?",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(kb, one_time_keyboard=True, resize_keyboard=True),
    )
    return BUDGET


async def budget(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    bud = update.message.text.strip()
    ctx.user_data["budget"] = bud

    if "Até R$200" in bud:
        await update.message.reply_text(
            "Obrigado pela honestidade! 🙏\n\n"
            "No momento não tenho um plano nessa faixa de investimento, "
            "mas continuo postando muito conteúdo gratuito!\n\n"
            "Me segue lá: 👉 @leleocarletti no Instagram 📲\n\n"
            "Quando tiver pronto para investir de verdade na sua transformação, "
            "pode voltar aqui! 💪",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END

    await update.message.reply_text(
        "Perfeito! Você está pronto(a) para mudar de vida. 🚀\n\n"
        "Me passa o seu *número de WhatsApp com DDD* "
        "para o Leonardo entrar em contato:\n\n"
        "Ex: 11999999999",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove(),
    )
    return CONTATO


async def contato(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["contato"] = update.message.text.strip()
    kb = [
        ["Manhã — 8h às 12h", "Tarde — 12h às 18h"],
        ["Noite — 18h às 22h", "Qualquer horário"],
    ]
    await update.message.reply_text(
        "Ótimo! Qual o *melhor horário* para o Leonardo te ligar?",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(kb, one_time_keyboard=True, resize_keyboard=True),
    )
    return HORARIO


async def horario(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["horario"] = update.message.text.strip()
    d = ctx.user_data

    msg = (
        f"🔥 NOVO LEAD QUALIFICADO — CARLETTI COACHING\n\n"
        f"👤 Nome: {d['nome']}\n"
        f"🎯 Objetivo: {d['objetivo']}\n"
        f"⚖️ Meta de emagrecimento: {d['quanto']}\n"
        f"📋 Histórico: {d['tentou']}\n"
        f"🏋️ Disponibilidade de treino: {d['disponibilidade']}\n"
        f"💰 Budget mensal: {d['budget']}\n"
        f"📱 WhatsApp: {d['contato']}\n"
        f"🕐 Melhor horário para contato: {d['horario']}\n\n"
        f"⚡ Lead veio do bot de qualificação no Telegram."
    )

    try:
        await ctx.bot.send_message(chat_id=OWNER_CHAT_ID, text=msg)
        logger.info(f"Lead qualificado enviado: {d['nome']} | {d['contato']}")
    except Exception as e:
        logger.error(f"Erro ao notificar dono: {e}")

    await update.message.reply_text(
        f"Incrível, {d['nome']}! ✅\n\n"
        "Suas informações foram enviadas para o Leonardo.\n"
        "Ele vai entrar em contato com você pelo WhatsApp em breve! 📲\n\n"
        "Enquanto isso, já vai se inspirando:\n"
        "👉 @leleocarletti no Instagram 🚀",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


async def cancelar(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Tudo bem! Se mudar de ideia é só mandar /start 😊",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


async def erro_handler(update: object, ctx: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Erro no bot: {ctx.error}")


def main():
    if not TOKEN:
        raise ValueError("TELEGRAM_TOKEN não definido nas variáveis de ambiente!")

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
