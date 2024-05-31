from email.message import EmailMessage

from pydantic import EmailStr

from config import settings


def create_booking_confirmation_template(
        booking:dict,
        email_to:EmailStr,
):
    email = EmailMessage()
    email['subject'] = 'подтверждение бронирования'
    email['from']  = settings.SMTP_USER
    email['to'] = email_to

    email.set_content(
        f"""
                <h1>Подтвердите бронивароние</h1>
                Вы забронировали отель {booking['date_from']} по {booking['date_to']}
                """,
        subtype='html'
    )
    return email