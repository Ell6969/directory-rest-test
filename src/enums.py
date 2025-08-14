import enum


class ContactTypeEnum(str, enum.Enum):
    PHONE = "phone"
    EMAIL = "email"
    TELEGRAM = "telegram"
    WHATSAPP = "whatsapp"
    OTHER = "other"
