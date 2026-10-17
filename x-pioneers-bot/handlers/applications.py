"""Join the Team application FSM handlers."""

from __future__ import annotations

import logging
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.admin import get_application_review_keyboard
from keyboards.main_menu import get_back_to_main_keyboard
from services.application_service import ApplicationService
from services.notification_service import NotificationService
from states.application_states import ApplicationSG

logger = logging.getLogger("xpioneers.handlers.applications")
router = Router(name="applications_router")


# ---------------- START APPLICATION FLOW ----------------

@router.callback_query(F.data == "nav_join")
async def start_application_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.clear()
    await state.set_state(ApplicationSG.waiting_for_name)

    intro_text = (
        "🤝 <b>Join X PIONEERS!</b>\n\n"
        "We are always excited to collaborate with passionate developers, 3D artists, "
        "educators, and innovators.\n\n"
        "Please fill out our quick 4-step application.\n"
        "<i>(You can type /cancel anytime to cancel the process.)</i>\n\n"
        "👉 <b>Step 1/4:</b> What is your full or preferred display name?"
    )

    if callback.message:
        await callback.message.edit_text(
            text=intro_text,
            parse_mode="HTML",
        )


@router.message(Command("join"))
async def start_application_command(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(ApplicationSG.waiting_for_name)
    await message.answer(
        "🤝 <b>Join X PIONEERS!</b>\n\n"
        "Please fill out our quick 4-step application.\n"
        "<i>(You can type /cancel anytime to cancel the process.)</i>\n\n"
        "👉 <b>Step 1/4:</b> What is your full or preferred display name?",
        parse_mode="HTML",
    )


# ---------------- CANCELLATION ----------------

@router.message(Command("cancel"))
async def command_cancel(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        await message.answer(
            "Nothing is currently active to cancel.",
            reply_markup=get_back_to_main_keyboard(),
        )
        return

    await state.clear()
    await message.answer(
        "❌ Application or action cancelled. You can return to the main menu whenever you're ready.",
        reply_markup=get_back_to_main_keyboard(),
    )


@router.callback_query(F.data == "app_cancel")
async def callback_cancel_application(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.answer("Application cancelled.", show_alert=False)
    if callback.message:
        await callback.message.edit_text(
            "❌ Application cancelled. No data was saved.",
            reply_markup=get_back_to_main_keyboard(),
        )


# ---------------- FSM STEP HANDLERS ----------------

@router.message(ApplicationSG.waiting_for_name)
async def process_name(message: Message, state: FSMContext) -> None:
    raw_text = message.text or ""
    valid, error = ApplicationService.validate_name(raw_text)
    if not valid:
        await message.answer(f"⚠️ {error}\n\nPlease enter your name:")
        return

    await state.update_data(name=raw_text.strip())
    await state.set_state(ApplicationSG.waiting_for_interest)
    await message.answer(
        "👉 <b>Step 2/4:</b> What area are you most interested in?\n"
        "<i>(e.g., AI/ML, Python Backend, Frontend, 3D/EdTech, Content, Community)</i>",
        parse_mode="HTML",
    )


@router.message(ApplicationSG.waiting_for_interest)
async def process_interest(message: Message, state: FSMContext) -> None:
    raw_text = message.text or ""
    valid, error = ApplicationService.validate_interest(raw_text)
    if not valid:
        await message.answer(f"⚠️ {error}\n\nPlease enter your area of interest:")
        return

    await state.update_data(interest=raw_text.strip())
    await state.set_state(ApplicationSG.waiting_for_skills)
    await message.answer(
        "👉 <b>Step 3/4:</b> What skills, tech stack, or relevant experience do you have?\n"
        "<i>(Don't worry if you're a beginner — enthusiasm and willingness to learn matter most!)</i>",
        parse_mode="HTML",
    )


@router.message(ApplicationSG.waiting_for_skills)
async def process_skills(message: Message, state: FSMContext) -> None:
    raw_text = message.text or ""
    valid, error = ApplicationService.validate_skills(raw_text)
    if not valid:
        await message.answer(f"⚠️ {error}\n\nPlease tell us about your skills:")
        return

    await state.update_data(skills=raw_text.strip())
    await state.set_state(ApplicationSG.waiting_for_motivation)
    await message.answer(
        "👉 <b>Step 4/4:</b> Why do you want to join X PIONEERS?\n"
        "<i>(Tell us what motivates you or what project you'd like to work on!)</i>",
        parse_mode="HTML",
    )


@router.message(ApplicationSG.waiting_for_motivation)
async def process_motivation(message: Message, state: FSMContext) -> None:
    raw_text = message.text or ""
    valid, error = ApplicationService.validate_motivation(raw_text)
    if not valid:
        await message.answer(f"⚠️ {error}\n\nPlease share your motivation:")
        return

    await state.update_data(motivation=raw_text.strip())
    await state.set_state(ApplicationSG.reviewing)

    data = await state.get_data()
    review_text = ApplicationService.format_review(data)

    await message.answer(
        text=review_text,
        parse_mode="HTML",
        reply_markup=get_application_review_keyboard(),
    )


# ---------------- REVIEW & SUBMISSION ----------------

@router.callback_query(F.data == "app_restart", ApplicationSG.reviewing)
async def callback_restart_application(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.clear()
    await state.set_state(ApplicationSG.waiting_for_name)
    if callback.message:
        await callback.message.edit_text(
            "🔄 Form restarted.\n\n"
            "👉 <b>Step 1/4:</b> What is your full or preferred display name?",
            parse_mode="HTML",
        )


@router.callback_query(F.data == "app_confirm_submit", ApplicationSG.reviewing)
async def callback_confirm_submission(
    callback: CallbackQuery,
    state: FSMContext,
    application_service: ApplicationService,
    notification_service: NotificationService,
) -> None:
    await callback.answer()
    data = await state.get_data()

    user = callback.from_user
    if not user:
        return

    try:
        app_id = await application_service.submit_application(
            user_id=user.id,
            username=user.username,
            data=data,
        )

        # Notify leadership immediately
        await notification_service.notify_admins_new_application(
            app_id=app_id,
            applicant_id=user.id,
            username=user.username,
            data=data,
        )

        await state.clear()

        success_text = (
            "🎉 <b>Application Submitted Successfully!</b>\n\n"
            f"Thank you, <b>{data.get('name')}</b>! Your application (ID: #{app_id}) has been forwarded "
            "directly to the X PIONEERS leadership team.\n\n"
            "We review every application thoroughly and will reach out via Telegram.\n\n"
            "💡 <i>One Team. One Vision. A Bigger Future.</i>"
        )

        if callback.message:
            await callback.message.edit_text(
                text=success_text,
                parse_mode="HTML",
                reply_markup=get_back_to_main_keyboard(),
            )
    except Exception as e:
        logger.error("Error submitting application: %s", e)
        await callback.answer("An error occurred while saving your application. Please try again.", show_alert=True)
